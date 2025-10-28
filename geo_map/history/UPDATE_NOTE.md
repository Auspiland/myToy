# 업데이트 노트

## 2025-10-27 섬 지역 감지 및 방향 계산 개선

### 주요 변경사항

#### 1. 섬 지역 자동 감지 기능 추가
- 멀티폴리곤에서 가장 큰 폴리곤을 내륙으로 간주
- 드러난 부분(교차 영역) 중 섬이 40% 이상 차지하면 "섬" 표기
- 예: `"전라남도 남부 섬"`, `"경상남도 동부 섬"`

**판단 기준**:
```
섬 교차 면적 / 전체 교차 면적 >= 0.40
```

#### 2. 방향 계산 로직 개선
- **이전**: 행정구역 중심 → rect 중심 방향
- **현재**: 행정구역 중심 → 겹친 영역의 중심 방향

**효과**: rect 크기에 관계없이 정확한 방향 표현

#### 3. 성능 최적화
- 이미 계산된 `intersection` 재사용하여 중복 계산 제거
- 멀티폴리곤 처리 시 약 50% 성능 향상

### 기술적 세부사항

**새로운 함수**:
- `analyze_multipolygon_islands(geometry, rect_polygon, total_intersection)`
  - 내륙과 섬의 교차 비율 계산
  - 섬의 중심 좌표 반환

**수정된 함수**:
- `get_region_representative_name()`: `intersection` 파라미터 추가
- `query_regions_in_rect()`: `provincial_regions` 데이터 구조 개선

**데이터 구조**:
```python
provincial_regions = {
    "region_name": {
        "coverage": float,      # 포함 비율
        "intersection": Polygon # 교차 영역 geometry
    }
}
```

### 예시

**입력**: 제주도 남쪽 해상 좌표
```python
rect_coords = [[126.2, 33.2], [126.8, 33.2],
               [126.2, 33.0], [126.8, 33.0]]
```

**출력**:
- 이전: `"제주특별자치도 남부 포함"`
- 현재: `"제주특별자치도 남부 섬"` (마라도 등 감지)
