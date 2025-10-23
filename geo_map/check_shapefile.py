import os
import json
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, mapping

BASE_PATH = r"C:\Users\T3Q\jeonghan\Eunhyea_Asist\geo_map"
NSKOREA = os.path.join(BASE_PATH, "ns_korea_shp")
N_KOREA = os.path.join(BASE_PATH, "prk_adm_wfp_20190624_shp")


def list_shp_files(DIR: str):
    """DIR 하위의 모든 .shp 파일 경로 리스트 반환(재귀)."""
    shp_files = []
    for root, _, files in os.walk(DIR):
        for file in files:
            if file.lower().endswith(".shp"):
                shp_files.append(os.path.join(root, file))
    return shp_files

def _pick_first_existing_col(df, candidates):
    """candidates 중 df에 존재하는 첫 번째 컬럼명 반환. 없으면 None."""
    for c in candidates:
        if c in df.columns:
            return c
    return None

def print_boundaries(DIR: str, FULL: bool = False, PREVIEW_COORDS: int = 10):
    """
    DIR 하위의 모든 Shapefile에 대해 각 지역의 경계 좌표를 출력.
    - FULL=False: 좌표 일부만 미리보기
    - FULL=True : 전체 좌표 출력(데이터가 매우 클 수 있음)
    """
    shp_list = list_shp_files(DIR)
    if not shp_list:
        print("(no .shp files found)")
        return

    for shp in shp_list:
        try:
            gdf = gpd.read_file(shp)
        except Exception as e:
            print(f"[READ FAIL] {shp} -> {e}")
            continue

        name_col = _pick_first_existing_col(
            gdf, ["name", "NAME", "Name", "adm_nm", "ADM_NM", "sig_kor_nm", "EMD_KOR_NM", "시군구명칭", "읍면동명칭"]
        )

        print(f"\n=== {shp} ===")
        print("Columns:", list(gdf.columns))
        if name_col:
            print(f"(name column: {name_col})")
        else:
            print("(name column not found; will use row index as name)")

        for idx, row in gdf.iterrows():
            geom = row.geometry
            if geom is None or geom.is_empty:
                continue

            # 이름
            nm = str(row[name_col]) if name_col else f"feature_{idx}"

            # Polygon/MultiPolygon만 처리(그 외 타입은 스킵)
            if isinstance(geom, Polygon):
                geoms = [geom]
            elif isinstance(geom, MultiPolygon):
                geoms = list(geom.geoms)
            else:
                # 필요하면 LineString/Point도 처리 가능
                # 여기서는 경계(면)만 대상으로 함
                continue

            # GeoJSON 형식으로 좌표 뽑기
            # MultiPolygon -> coordinates: [ [ [x,y], ... ],  # polygon 1 외곽/홀
            #                               [ [x,y], ... ],  # polygon 2 ...
            #                             ]
            gj = mapping(MultiPolygon(geoms) if len(geoms) > 1 else geoms[0])
            coords = gj.get("coordinates", [])

            # 출력(미리보기 / 전체)
            if FULL:
                print(json.dumps(
                    {"name": nm, "type": gj.get("type"), "coordinates": coords},
                    ensure_ascii=False
                ))
            else:
                # 앞쪽 좌표 PREVIEW_COORDS개만 미리보기
                # 구조가 중첩이므로, 평탄화된 앞부분 샘플을 만든다.
                preview = []
                def _collect_preview(cs, limit):
                    # cs: 중첩 좌표(폴리곤/멀티폴리곤)
                    # limit: 남은 수
                    if limit <= 0:
                        return 0
                    if isinstance(cs, (list, tuple)) and len(cs) > 0 and isinstance(cs[0], (list, tuple)):
                        # 더 중첩
                        for c in cs:
                            limit = _collect_preview(c, limit)
                            if limit <= 0:
                                break
                        return limit
                    else:
                        # 좌표 한 점([x,y])로 간주
                        preview.append(cs)
                        return limit - 1

                _ = _collect_preview(coords, PREVIEW_COORDS)
                print(json.dumps(
                    {"name": nm, "type": gj.get("type"), "preview_coords": preview, "note": f"preview first {PREVIEW_COORDS} points"},
                    ensure_ascii=False
                ))

def convert2json(file):
    gdf = gpd.read_file(file)
    base_name = os.path.splitext(os.path.basename(file))[0]
    out_path = os.path.join(os.path.dirname(file), f"{base_name}.geojson")
    gdf.to_file(out_path, driver="GeoJSON", encoding="utf-8")

def convert2json_dir(DIR):
    shp_list = list_shp_files(DIR)
    if not shp_list:
        print("(no .shp files found)")
        return False
    
    for shp_now in shp_list:
        convert2json(shp_now)
    return True

def print_infos_dir(DIR):
    # shapefile 읽기
    for file_path in list_shp_files(DIR):
        try:
            gdf = gpd.read_file(file_path)  # Shapefile은 .cpg 기준 인코딩 자동 처리
        except Exception as e:
            print(f"[READ FAIL] {file_path} -> {e}")
            continue

        print(f"\n=== {file_path} ===")
        print("Columns:", list(gdf.columns))

        # fclass 대체 후보(데이터셋에 따라 다름)
        fclass_col = _pick_first_existing_col(gdf, ["fclass", "place", "type", "class", "category", "layer"])
        if fclass_col:
            try:
                print(f"Unique {fclass_col} values:", sorted(gdf[fclass_col].dropna().astype(str).unique()))
            except Exception:
                print(f"(warn) {fclass_col} 고유값 출력 중 오류")
        else:
            print("No fclass-like column found. (tried: fclass/place/type/class/category/layer)")

        # 도/시/군/구 수준 필터링용 타겟 라벨(데이터셋에 맞춰 조정 가능)
        # OSM places 기준으로는 city/county가 흔함. region은 없을 수도 있음.
        admin_levels = ['region', 'city', 'county']

        # population 대체 후보
        pop_col = _pick_first_existing_col(
            gdf, ["population", "pop", "POP", "POPULATION", "pop_max", "pop_min"]
        )

        if not fclass_col:
            print("(skip) 분류 컬럼이 없어 레벨별 집계를 건너뜁니다.")
            # 최소한 이름 상위 10개만 출력
            name_col = _pick_first_existing_col(gdf, ["name", "NAME", "Name"])
            if name_col:
                print("Sample names (top 10):")
                for nm in gdf[name_col].dropna().astype(str).head(10):
                    print("  ", nm)
            continue

        for fc in admin_levels:
            subset = gdf[gdf[fclass_col].astype(str) == fc]
            print(f'\n[{fc}] - Total: {len(subset)}')

            if len(subset) == 0:
                continue

            name_col = _pick_first_existing_col(subset, ["name", "NAME", "Name"])
            if pop_col and pop_col in subset.columns:
                # 숫자형 보장
                sub2 = subset.copy()
                sub2[pop_col] = pd.to_numeric(sub2[pop_col], errors="coerce")
                subset_sorted = sub2.sort_values(pop_col, ascending=False)
                print(f"Top 10 by {pop_col}:")
                cols_to_show = [c for c in [name_col, pop_col] if c]
                for _, row in subset_sorted[cols_to_show].head(10).iterrows():
                    nm = row[name_col] if name_col else "(no name)"
                    pv = row[pop_col]
                    print(f"  {nm} (pop: {pv})")
            else:
                # 인구 컬럼이 없으면 이름 기준 상위 10개만
                if name_col:
                    print("Top 10 (no population column):")
                    for nm in subset[name_col].dropna().astype(str).head(10):
                        print(f"  {nm}")
                else:
                    print("(no name/population columns to display)")


def describe_shapefile(shp_path: str, sample_n: int = 5):
    """
    지정한 shapefile의 기본 정보를 출력하는 함수.
    - shp_path: .shp 파일 경로
    - sample_n: 미리보기로 출력할 행(row) 개수
    """
    if not os.path.exists(shp_path):
        print(f"[ERROR] 파일을 찾을 수 없습니다: {shp_path}")
        return

    try:
        gdf = gpd.read_file(shp_path)
    except Exception as e:
        print(f"[ERROR] 파일을 읽는 중 오류 발생: {e}")
        return

    print(f"\n=== Shapefile 정보: {shp_path} ===")
    print(f"- 파일 이름: {os.path.basename(shp_path)}")
    print(f"- 총 객체(Feature) 수: {len(gdf)}")
    print(f"- 좌표계(CRS): {gdf.crs}")
    print(f"- Geometry 타입: {gdf.geom_type.unique()}")
    print(f"- 컬럼 목록: {list(gdf.columns)}")

    # 주요 속성 컬럼 미리보기
    non_geom_cols = [c for c in gdf.columns if c != "geometry"]
    if non_geom_cols:
        print("\n[속성 미리보기]")
        print(gdf[non_geom_cols].head(sample_n).to_string(index=False))
    else:
        print("\n(속성 컬럼이 없습니다)")

    # Geometry 요약
    try:
        bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
        centroid = gdf.geometry.unary_union.centroid
        print("\n[공간 범위]")
        print(f"  - 최소경도(minx): {bounds[0]:.6f}")
        print(f"  - 최소위도(miny): {bounds[1]:.6f}")
        print(f"  - 최대경도(maxx): {bounds[2]:.6f}")
        print(f"  - 최대위도(maxy): {bounds[3]:.6f}")
        print(f"  - 중심점(centroid): ({centroid.x:.6f}, {centroid.y:.6f})")
    except Exception as e:
        print(f"\n(geometry 요약 계산 실패: {e})")

    print("====================================\n")



def describe_shapefile_dir(DIR):
    # shapefile 읽기
    for file_path in list_shp_files(DIR):
        describe_shapefile(file_path)

# 실행 예시
if __name__ == "__main__":
    # 미리보기(좌표 10개)
    # print_boundaries(NSKOREA, FULL=False, PREVIEW_COORDS=10)

    # print_infos_dir(N_KOREA)
    # describe_shapefile_dir(N_KOREA)

    filepath = os.path.join(NSKOREA, "kontur_boundaries_KR_20220407.gpkg")
    # describe_shapefile(filepath)

    convert2json(filepath)

    # 전체 좌표 출력(매우 방대할 수 있음)
    # print_boundaries(SOUTH_KOREA, FULL=True)