import json
from collections import OrderedDict

# LLM 호출 함수 (사용자가 제공)
from src.common_utils import response_GPT


def collect_unique_names(geojson):
    """ADM0_EN/ADM1_EN/ADM2_EN의 영어 지명 유니크 집합 수집"""
    names = set()
    for feat in geojson.get("features", []):
        props = feat.get("properties", {}) or {}
        for k in ("ADM0_EN", "ADM1_EN", "ADM2_EN"):
            v = props.get(k)
            if isinstance(v, str) and v.strip():
                names.add(v.strip())
    return sorted(names)


def translate_names_with_llm(eng_names, seed_map=None):
    """
    영어 이름 리스트를 LLM으로 한국어로 번역해 dict 반환.
    LLM 출력 형식은 {"English Name":"한국어"} JSON 딕셔너리로 요구.
    """
    seed_map = seed_map or {}
    todo = [n for n in eng_names if n not in seed_map]

    if not todo:
        return dict(seed_map)

    system_prompt = (
        "You are a precise translation engine. Translate each administrative unit name into Korean "
        "using official/common Korean exonyms. Return ONLY valid JSON object mapping English->Korean. "
        "Do not add comments."
    )
    # JSON 배열로 입력, JSON 객체로 응답 강제
    user_prompt = (
        "Translate the following English administrative names to Korean. "
        "Return a JSON object where keys are the exact English strings and values are the Korean translations.\n\n"
        f"{json.dumps(todo, ensure_ascii=False)}"
    )

    resp = response_GPT(system_prompt=system_prompt, user_prompt=user_prompt)

    # LLM이 코드블럭/텍스트를 감싸는 경우 대비, 최초/최후 중괄호만 추출
    start = resp.find("{")
    end = resp.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("LLM 응답에서 JSON 객체를 찾을 수 없습니다.")

    llm_json_text = resp[start : end + 1]
    llm_map = json.loads(llm_json_text)

    # 시드와 병합
    out = dict(seed_map)
    out.update({k: v for k, v in llm_map.items() if isinstance(k, str) and isinstance(v, str)})
    return out


def insert_ko_and_prune(props, en2ko):
    """
    properties의 키 순서를 최대한 보존하면서
    - ADM0_EN/ADM1_EN/ADM2_EN 뒤에 각각 ADM0_KO/ADM1_KO/ADM2_KO 삽입
    - 'ADM2_REF','ADM2ALT1EN','ADM2ALT2EN' 제거
    """
    remove_keys = {"ADM2_REF", "ADM2ALT1EN", "ADM2ALT2EN"}
    out = OrderedDict()
    for k, v in props.items():
        if k in remove_keys:
            # 명시적으로 삭제
            continue

        out[k] = v

        if k in ("ADM0_EN", "ADM1_EN", "ADM2_EN"):
            ko_key = k.replace("_EN", "_KO")
            en_val = v if isinstance(v, str) else None
            ko_val = en2ko.get(en_val) if en_val else None
            out[ko_key] = ko_val

    # 혹시 EN 키가 전혀 없었는데 KO를 따로 요구한다면, 추가하지 않음(요구 사항: 비슷한 위치에만 삽입)
    return out


def process_geojson(in_path, out_path, seed_map=None):
    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1) 영어 이름 수집
    eng_names = collect_unique_names(data)

    # 2) LLM으로 번역 맵 생성
    en2ko = translate_names_with_llm(eng_names, seed_map=seed_map)

    # 3) 각 feature에 KO 필드 삽입 + 불필요 키 제거
    for feat in data.get("features", []):
        props = feat.get("properties", {}) or {}
        feat["properties"] = insert_ko_and_prune(props, en2ko)

    # 4) 결과 저장
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    # 5) dict 출력 (필요 시 반환)
    print(json.dumps(en2ko, ensure_ascii=False, indent=2))
    return en2ko


def apply_fix_table(in_path, out_path, fix_table):
    """GeoJSON 파일을 읽어 fix_table의 수정사항을 적용"""
    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for feat in data.get("features", []):
        props = feat.get("properties", {}) or {}

        # 한글 키 수정
        for k in ("ADM0_KO", "ADM1_KO", "ADM2_KO"):
            v = props.get(k)
            if isinstance(v, str) and v in fix_table:
                props[k] = fix_table[v]

        # 영문 키 수정
        for k in ("ADM0_EN", "ADM1_EN", "ADM2_EN"):
            v = props.get(k)
            if isinstance(v, str) and v in fix_table:
                props[k] = fix_table[v]

        feat["properties"] = props

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# -------------------- 사용 예 --------------------
seed_map = {"Democratic People's Republic of Korea (the)": "조선민주주의인민공화국"}
process_geojson(
    in_path=r"C:\Users\T3Q\jeonghan\Eunhyea_Asist\geo_map\prk_adm_wfp_20190624_shp\prk_admbnda_adm2_wfp_20190624.geojson",
    out_path=r"C:\Users\T3Q\jeonghan\Eunhyea_Asist\geo_map\prk_adm_wfp_20190624_shp\new_prk_admbnda_adm2_wfp_20190624.geojson",
    seed_map=seed_map
)

fix_table = {
    "장도군": "창도군",          # Changdo
    "청남군": "청남구역",        # Chongnam
    "수동구역": "수동군",        # Sudong
    "영변군": "녕변군",          # Nyongbyon
    "영원군": "녕원군",          # Nyongwon
    "삼지연군": "삼지연시",      # Samjiyon
    "Jaerong": "Jaeryong",       # 영문 표기 수정 권장
    "Kophung": "Kopung",         # 영문 표기 수정 권장
    "Taegwan": "Daegwan",        # 영문 표기 통일
}
file = r"C:\Users\T3Q\jeonghan\Eunhyea_Asist\geo_map\prk_adm_wfp_20190624_shp\new_prk_admbnda_adm2_wfp_20190624.geojson"

apply_fix_table(file,file,fix_table)
