import os
import re
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, Point
from shapely.validation import make_valid

# -------------------------------
# 설정 (기존과 동일)
# -------------------------------
BASE_PATH = r"C:\Users\T3Q\jeonghan\Eunhyea_Assist\geo_map"
SOUTH_KOREA = os.path.join(BASE_PATH, "south-korea-251021-free.shp")
NORTH_KOREA = os.path.join(BASE_PATH, "north-korea-251021-free.shp")

# 시도코드,시도명칭,시군구코드,시군구명칭,읍면동코드,읍면동명칭
REGION_MAPPING_S = os.path.join(BASE_PATH, "SGIS 행정구역 코드202406.csv")
# 일련번호,시도,시군구,면적,아이디
REGION_MAPPING_N = os.path.join(BASE_PATH, "통계청_원격탐사_북한행정지역_20210826.csv")

PLACES_POLYGON_PATH_S = os.path.join(SOUTH_KOREA, "gis_osm_places_a_free_1.shp")
PLACES_POINT_PATH_S   = os.path.join(SOUTH_KOREA, "gis_osm_places_free_1.shp")

PLACES_POLYGON_PATH_N = os.path.join(NORTH_KOREA, "gis_osm_places_a_free_1.shp")
PLACES_POINT_PATH_N   = os.path.join(NORTH_KOREA, "gis_osm_places_free_1.shp")

NAME_COL = "name"
SRC_CRS = "EPSG:4326"
AREA_CRS = "EPSG:5179"

# -------------------------------
# 공통 함수
# -------------------------------

def load_and_merge_shapefiles(paths, name_col, src_crs):
    """여러 shapefile을 읽고 병합"""
    frames = []
    for path in paths:
        if not os.path.exists(path):
            continue
        try:
            gdf = gpd.read_file(path)
            if gdf.crs is None:
                gdf.set_crs(src_crs, inplace=True)
            gdf = gdf[gdf[name_col].notna() & (gdf[name_col] != "")]
            frames.append(gdf)
        except Exception as e:
            print(f"파일 로드 실패: {path}, 오류: {e}")
    if frames:
        merged = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=src_crs)
        merged["geometry"] = merged["geometry"].apply(make_valid)
        return merged
    return gpd.GeoDataFrame(columns=[name_col, "geometry"], crs=src_crs)

# -------------------------------
# 중앙 박스(비율)
# -------------------------------

def _center_box_polygon_ratio(rect_coords, ratio=0.30):
    """
    직사각형(rect_coords) 내부의 '가운데 ratio' 박스를 생성.
    반환: (inner_poly_wgs84(SRC_CRS), inner_poly_m(AREA_CRS))
    """
    xs, ys = zip(*rect_coords)
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    mx = (1.0 - ratio) / 2.0
    my = (1.0 - ratio) / 2.0
    in_minx = minx + (maxx - minx) * mx
    in_maxx = maxx - (maxx - minx) * mx
    in_miny = miny + (maxy - miny) * my
    in_maxy = maxy - (maxy - miny) * my

    inner_poly_wgs84 = Polygon([
        (in_minx, in_miny), (in_maxx, in_miny),
        (in_maxx, in_maxy), (in_minx, in_maxy)
    ])
    inner_gdf = gpd.GeoDataFrame(geometry=[inner_poly_wgs84], crs=SRC_CRS).to_crs(AREA_CRS)
    inner_poly_m = inner_gdf.geometry.iloc[0]
    return inner_poly_wgs84, inner_poly_m

def _filter_center_box_points(gdf, inner_poly_m):
    """
    gdf(AREA_CRS) 의 포인트(또는 폴리곤의 대표 포인트)가 inner_poly_m 안에 있는 것만 필터링.
    입력 gdf는 반드시 AREA_CRS 이어야 함.
    """
    geom = gdf.geometry
    rep_points = geom.apply(lambda g: g if g.geom_type == "Point" else g.representative_point())
    return gdf[rep_points.within(inner_poly_m)].copy()

# -------------------------------
# 지역명 정규화 & 매핑 로더
# -------------------------------

_norm_suffix_pattern = re.compile(r"(특별자치도|특별자치시|광역시|자치시|자치구|특별시|시|군|구|읍|면|동|도)$")

def _normalize_name(s: str) -> str:
    """
    - 괄호 및 괄호 내 부가표기 제거
    - 슬래시/쉼표 다국어 표기 분리 시 첫 토큰 사용
    - 행정접미사 제거(시/군/구/읍/면/동 등)
    - 공백 제거, 소문자화
    """
    if s is None:
        return ""
    s = str(s).strip()
    # 다국어 표기 구분자 처리(예: "Seoul/서울/ソウル")
    if "/" in s:
        s = s.split("/")[0].strip()
    if "," in s:
        s = s.split(",")[0].strip()
    # 괄호 제거
    s = re.sub(r"\(.*?\)", "", s).strip()
    # 접미 행정단위 제거(여러 번 적용 가능)
    prev = None
    while prev != s:
        prev = s
        s = _norm_suffix_pattern.sub("", s).strip()
    # 공백 제거 및 소문자
    s = s.replace(" ", "").lower()
    return s

# 캐시
_S_EMD = None   # 읍면동 → (시군구, 시도)
_S_SGG = None   # 시군구 → (시도)
_S_SIDO = None  # 시도 set
_N_SGG = None   # 시군구 → (시도)
_N_SIDO = None  # 시도 set

def _load_region_mapping_south(csv_path: str):
    global _S_EMD, _S_SGG, _S_SIDO
    if _S_EMD is not None:
        return
    if not os.path.exists(csv_path):
        _S_EMD, _S_SGG, _S_SIDO = {}, {}, set()
        return
    # 인코딩 가변 처리
    for enc in ("utf-8-sig", "cp949", "euc-kr"):
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            break
        except Exception:
            df = None
    if df is None:
        _S_EMD, _S_SGG, _S_SIDO = {}, {}, set()
        return

    # 컬럼 표준화
    cols = df.columns.tolist()
    # 예상 컬럼명 존재 여부 확인
    need = {"시도명칭", "시군구명칭", "읍면동명칭"}
    if not need.issubset(set(cols)):
        # 헤더가 다르면 스킵
        _S_EMD, _S_SGG, _S_SIDO = {}, {}, set()
        return

    _S_EMD = {}
    _S_SGG = {}
    _S_SIDO = set()

    for _, r in df.iterrows():
        sido = str(r["시도명칭"]).strip()
        sgg  = str(r["시군구명칭"]).strip() if pd.notna(r["시군구명칭"]) else ""
        emd  = str(r["읍면동명칭"]).strip() if pd.notna(r["읍면동명칭"]) else ""
        if sido:
            _S_SIDO.add(_normalize_name(sido))
        if sgg:
            _S_SGG[_normalize_name(sgg)] = (sgg, sido)
        if emd:
            _S_EMD[_normalize_name(emd)] = (emd, sgg, sido)

def _load_region_mapping_north(csv_path: str):
    global _N_SGG, _N_SIDO
    if _N_SGG is not None:
        return
    if not os.path.exists(csv_path):
        _N_SGG, _N_SIDO = {}, set()
        return
    for enc in ("utf-8-sig", "cp949", "euc-kr"):
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            break
        except Exception:
            df = None
    if df is None:
        _N_SGG, _N_SIDO = {}, set()
        return

    # 예상 컬럼명: 시도, 시군구
    if not {"시도", "시군구"}.issubset(set(df.columns)):
        _N_SGG, _N_SIDO = {}, set()
        return

    _N_SGG = {}
    _N_SIDO = set()
    for _, r in df.iterrows():
        sido = str(r["시도"]).strip() if pd.notna(r["시도"]) else ""
        sgg  = str(r["시군구"]).strip() if pd.notna(r["시군구"]) else ""
        if sido:
            _N_SIDO.add(_normalize_name(sido))
        if sgg:
            _N_SGG[_normalize_name(sgg)] = (sgg, sido)

def _best_partial_key_match(keys, target_key: str):
    """
    keys: 정규화된 키들의 이터러블(예: _S_EMD.keys())
    target_key: 정규화된 비교 대상(예: _normalize_name('천안시'))

    반환: (match_key, score)
      - match_key: 부분 포함이 성립한 키 (없으면 None)
      - score: 매칭 강도(길이 우선). 길이가 긴 키를 우선하여 가장 특이적인 것을 선택.
    """
    if not target_key:
        return None, 0

    best_k, best_score = None, 0
    for k in keys:
        if not k:
            continue
        # target이 key를 포함하거나, key가 target을 포함하면 후보
        if (k in target_key) or (target_key in k):
            # 더 긴 문자열일수록 더 특이적 → 점수는 길이 기준
            score = max(len(k), len(target_key))
            if score > best_score:
                best_k, best_score = k, score
    return best_k, best_score

def _find_parents(name: str):
    _load_region_mapping_south(REGION_MAPPING_S)
    _load_region_mapping_north(REGION_MAPPING_N)

    key = _normalize_name(name)
    if not key:
        return {}

    # ---------- 정확 매칭 ----------
    if key in (_S_EMD or {}):
        _, sgg, sido = _S_EMD[key]
        return {"country":"KR","level":"emd","parent_sgg":sgg,"parent_sido":sido,
                "match_source":"south-emd","name_match_type":"exact","name_match_score":len(key)}

    if key in (_S_SGG or {}):
        sgg, sido = _S_SGG[key]
        return {"country":"KR","level":"sgg","parent_sgg":None,"parent_sido":sido,
                "match_source":"south-sgg","name_match_type":"exact","name_match_score":len(key)}

    if key in (_S_SIDO or set()):
        return {"country":"KR","level":"sido","parent_sgg":None,"parent_sido":None,
                "match_source":"south-sido","name_match_type":"exact","name_match_score":len(key)}

    if key in (_N_SGG or {}):
        sgg, sido = _N_SGG[key]
        return {"country":"KP","level":"sgg","parent_sgg":None,"parent_sido":sido,
                "match_source":"north-sgg","name_match_type":"exact","name_match_score":len(key)}

    if key in (_N_SIDO or set()):
        return {"country":"KP","level":"sido","parent_sgg":None,"parent_sido":None,
                "match_source":"north-sido","name_match_type":"exact","name_match_score":len(key)}

    # ---------- 포함(contains) 매칭 ----------
    best = None
    def _pick(cand):
        nonlocal best
        if (best is None) or (cand["_score"] > best["_score"]):
            best = cand

    m_key, score = _best_partial_key_match((_S_EMD or {}).keys(), key)
    if m_key:
        emd, sgg, sido = _S_EMD[m_key]
        _pick({"country":"KR","level":"emd","parent_sgg":sgg,"parent_sido":sido,
               "match_source":"south-emd~contains","name_match_type":"contains",
               "name_match_score":score,"_score":score})

    m_key2, score2 = _best_partial_key_match((_S_SGG or {}).keys(), key)
    if m_key2:
        sgg, sido = _S_SGG[m_key2]
        _pick({"country":"KR","level":"sgg","parent_sgg":None,"parent_sido":sido,
               "match_source":"south-sgg~contains","name_match_type":"contains",
               "name_match_score":score2,"_score":score2})

    m_key3, score3 = _best_partial_key_match((_S_SIDO or set()), key)
    if m_key3:
        _pick({"country":"KR","level":"sido","parent_sgg":None,"parent_sido":None,
               "match_source":"south-sido~contains","name_match_type":"contains",
               "name_match_score":score3,"_score":score3})

    m_key4, score4 = _best_partial_key_match((_N_SGG or {}).keys(), key)
    if m_key4:
        sgg, sido = _N_SGG[m_key4]
        _pick({"country":"KP","level":"sgg","parent_sgg":None,"parent_sido":sido,
               "match_source":"north-sgg~contains","name_match_type":"contains",
               "name_match_score":score4,"_score":score4})

    m_key5, score5 = _best_partial_key_match((_N_SIDO or set()), key)
    if m_key5:
        _pick({"country":"KP","level":"sido","parent_sgg":None,"parent_sido":None,
               "match_source":"north-sido~contains","name_match_type":"contains",
               "name_match_score":score5,"_score":score5})

    if best:
        best.pop("_score", None)
        return best
    return {}


# -------------------------------
# 중앙 박스 내 도시군구 추출(+상위 지역 병기)
# -------------------------------

def list_regions_in_center_box(
    rect_coords,
    polygon_paths=None,
    point_paths=None,
    name_col=NAME_COL,
    center_ratio=0.30,
    fclass_allow=("city", "county")
):
    if polygon_paths is None:
        polygon_paths = [PLACES_POLYGON_PATH_S, PLACES_POLYGON_PATH_N]
    if point_paths is None:
        point_paths = [PLACES_POINT_PATH_S, PLACES_POINT_PATH_N]

    # 가운데 박스 생성 (ratio만 사용)
    inner_poly_wgs84, inner_poly_m = _center_box_polygon_ratio(rect_coords, ratio=center_ratio)

    # 사각형 중심점(거리 계산용)
    cx = (inner_poly_wgs84.bounds[0] + inner_poly_wgs84.bounds[2]) / 2.0
    cy = (inner_poly_wgs84.bounds[1] + inner_poly_wgs84.bounds[3]) / 2.0
    center_pt_m = gpd.GeoSeries([Point(cx, cy)], crs=SRC_CRS).to_crs(AREA_CRS).iloc[0]

    # 1) polygon
    gdf_poly = load_and_merge_shapefiles(polygon_paths, name_col, SRC_CRS)
    if len(gdf_poly) > 0:
        if 'fclass' in gdf_poly.columns and fclass_allow:
            gdf_poly = gdf_poly[gdf_poly['fclass'].isin(fclass_allow)]
        gdf_poly = gdf_poly.to_crs(AREA_CRS)
        gdf_poly_f = _filter_center_box_points(gdf_poly, inner_poly_m)
        if len(gdf_poly_f) > 0:
            gdf_poly_f = gdf_poly_f[[name_col, 'fclass', 'geometry']].copy()
            gdf_poly_f["type"] = "polygon"
        else:
            gdf_poly_f = gpd.GeoDataFrame(columns=[name_col, 'fclass', 'geometry', 'type'], crs=AREA_CRS)
    else:
        gdf_poly_f = gpd.GeoDataFrame(columns=[name_col, 'fclass', 'geometry', 'type'], crs=AREA_CRS)

    # 2) point
    gdf_pt = load_and_merge_shapefiles(point_paths, name_col, SRC_CRS)
    if len(gdf_pt) > 0:
        if 'fclass' in gdf_pt.columns and fclass_allow:
            gdf_pt = gdf_pt[gdf_pt['fclass'].isin(fclass_allow)]
        gdf_pt = gdf_pt.to_crs(AREA_CRS)
        gdf_pt_f = _filter_center_box_points(gdf_pt, inner_poly_m)
        if len(gdf_pt_f) > 0:
            gdf_pt_f = gdf_pt_f[[name_col, 'fclass', 'geometry']].copy()
            gdf_pt_f["type"] = "point"
        else:
            gdf_pt_f = gpd.GeoDataFrame(columns=[name_col, 'fclass', 'geometry', 'type'], crs=AREA_CRS)
    else:
        gdf_pt_f = gpd.GeoDataFrame(columns=[name_col, 'fclass', 'geometry', 'type'], crs=AREA_CRS)

    # 3) 합치고 중복 제거
    out = pd.concat([gdf_poly_f, gdf_pt_f], ignore_index=True) if len(gdf_poly_f) or len(gdf_pt_f) else \
          gpd.GeoDataFrame(columns=[name_col, 'fclass', 'geometry', 'type'], crs=AREA_CRS)
    if len(out) == 0:
        return out

    out = out.drop_duplicates(subset=[name_col, 'fclass', 'type']).reset_index(drop=True)
    out = gpd.GeoDataFrame(out, geometry='geometry', crs=AREA_CRS)

    # 4) 거리(distance_m) 계산: 대표점 사용
    rep_points = out.geometry.apply(lambda g: g if g.geom_type == "Point" else g.representative_point())
    out["distance_m"] = rep_points.distance(center_pt_m)

    # 5) 상위 지역/이름매칭 정보 추가
    for idx, row in out.iterrows():
        nm = row[name_col]
        info = _find_parents(nm) or {}
        out.at[idx, "parent_sgg"] = info.get("parent_sgg")
        out.at[idx, "parent_sido"] = info.get("parent_sido")
        out.at[idx, "country"] = info.get("country")
        out.at[idx, "level"] = info.get("level")
        out.at[idx, "match_source"] = info.get("match_source")
        out.at[idx, "name_match_type"] = info.get("name_match_type")
        out.at[idx, "name_match_score"] = info.get("name_match_score")

    # 6) 가까운 순서로 정렬
    out = out.sort_values(["distance_m", name_col]).reset_index(drop=True)

    return out

# -------------------------------
# 기존 대표 지역명 추출 함수(유지)
# -------------------------------
def get_representative_region(rect_coords,
                              polygon_paths=None,
                              point_paths=None,
                              name_col=NAME_COL):
    if polygon_paths is None:
        polygon_paths = [PLACES_POLYGON_PATH_S, PLACES_POLYGON_PATH_N]
    if point_paths is None:
        point_paths = [PLACES_POINT_PATH_S, PLACES_POINT_PATH_N]

    xs, ys = zip(*rect_coords)
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    rect_poly = Polygon([(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)])
    center_point = Point((minx + maxx) / 2, (miny + maxy) / 2)

    # Polygon 기반 (면적 교집합 최대)
    try:
        gdf = load_and_merge_shapefiles(polygon_paths, name_col, SRC_CRS)
        if 'fclass' in gdf.columns:
            gdf = gdf[gdf['fclass'].isin(['city', 'county'])]

        gdf = gdf.to_crs(AREA_CRS)
        rect_gdf = gpd.GeoDataFrame(geometry=[rect_poly], crs=SRC_CRS).to_crs(AREA_CRS)
        rect_poly_m = rect_gdf.geometry.iloc[0]

        gdf["inter_area"] = gdf.geometry.intersection(rect_poly_m).area
        candidates = gdf[gdf["inter_area"] > 0]

        if len(candidates) > 0:
            top = candidates.sort_values("inter_area", ascending=False).iloc[0]
            name = top[name_col]
            parent_info = _find_parents(name)
            return {
                "name": name,
                "type": "polygon",
                "fclass": top.get("fclass", "N/A"),
                "inter_area": float(top["inter_area"]),
                "total_area": float(rect_poly_m.area),
                "coverage_ratio": float(top["inter_area"] / rect_poly_m.area),
                **({} if not parent_info else {
                    "parent_sgg": parent_info.get("parent_sgg"),
                    "parent_sido": parent_info.get("parent_sido"),
                    "country": parent_info.get("country"),
                    "level": parent_info.get("level"),
                    "match_source": parent_info.get("match_source"),
                }),
            }

        raise ValueError("No polygon intersection found")

    except Exception as e:
        print(f"Polygon 기반 탐색 실패: {e}\nPoint 기반으로 전환합니다.")
        gdf = load_and_merge_shapefiles(point_paths, name_col, SRC_CRS)
        if 'fclass' in gdf.columns:
            gdf = gdf[gdf['fclass'].isin(['city', 'county'])]

        gdf = gdf.to_crs(AREA_CRS)
        center_gdf = gpd.GeoDataFrame(geometry=[center_point], crs=SRC_CRS).to_crs(AREA_CRS)
        center_point_m = center_gdf.geometry.iloc[0]

        gdf["distance"] = gdf.geometry.distance(center_point_m)
        top = gdf.sort_values("distance").iloc[0]
        name = top[name_col]
        parent_info = _find_parents(name)
        return {
            "name": name,
            "type": "point",
            "fclass": top.get("fclass", "N/A"),
            "distance_m": float(top["distance"]),
            "center_coord": (center_point.x, center_point.y),
            "place_coord": (top.geometry.x, top.geometry.y) if hasattr(top.geometry, 'x') else None,
            **({} if not parent_info else {
                "parent_sgg": parent_info.get("parent_sgg"),
                "parent_sido": parent_info.get("parent_sido"),
                "country": parent_info.get("country"),
                "level": parent_info.get("level"),
                "match_source": parent_info.get("match_source"),
            }),
        }

# -------------------------------
# 사용 예시
# -------------------------------
if __name__ == "__main__":
    rect_coords = [
        [126.93167575079963, 37.10178611970895],
        [127.50557082786963, 37.10314793150034],
        [126.93507098285538, 36.64210788827871],
        [127.50553754496315, 36.643447265652945]
    ]

    # 1) 중앙 박스 내 도시/군/구 목록 (ratio 방식만)
    gdf_center = list_regions_in_center_box(
        rect_coords,
        center_ratio=0.70  # 가운데 70%
    )
    print(f"[중앙 박스 포함 지역 수] {len(gdf_center)}")
    if len(gdf_center):
        # 이름 + 상위지역 간단 출력
        cols = [NAME_COL, "fclass", "type", "country", "level", "parent_sgg", "parent_sido", "match_source"]
        print(gdf_center[cols].head(30).to_string(index=False))

    # 2) 대표 지역명 하나 (상위지역 포함)
    # result = get_representative_region(rect_coords)
    # print("대표 지역명:", result)
