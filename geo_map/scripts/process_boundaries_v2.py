import json
import math
from typing import Tuple, List, Dict, Any

def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points (lon, lat)"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def find_closest_point_index(target: Tuple[float, float], coords: List[List[float]]) -> int:
    """Find the index of the closest coordinate to the target point"""
    min_dist = float('inf')
    min_idx = -1
    for i, coord in enumerate(coords):
        dist = distance(target, tuple(coord))
        if dist < min_dist:
            min_dist = dist
            min_idx = i
    return min_idx

def extract_polygon_coordinates(region_name: str, geojson_data: Dict[str, Any]) -> List[List[float]]:
    """Extract all coordinates from a region's polygon boundary as a flat list"""
    for feature in geojson_data['features']:
        props = feature['properties']
        if props.get('name') == region_name or props.get('adm1_ko') == region_name:
            geometry = feature['geometry']
            all_coords = []

            if geometry['type'] == 'MultiPolygon':
                for polygon in geometry['coordinates']:
                    for ring in polygon:
                        all_coords.extend(ring)
            elif geometry['type'] == 'Polygon':
                for ring in geometry['coordinates']:
                    all_coords.extend(ring)

            return all_coords
    return []

def extract_line_between_points(start_point: Tuple[float, float],
                                end_point: Tuple[float, float],
                                region_coords: List[List[float]],
                                max_distance: float = 0.02) -> List[List[float]]:
    """
    Extract the shortest path between two points on a polygon boundary.
    max_distance: maximum allowed distance from the boundary path
    """
    start_idx = find_closest_point_index(start_point, region_coords)
    end_idx = find_closest_point_index(end_point, region_coords)

    print(f"Start index: {start_idx}, End index: {end_idx}")
    print(f"Start coord: {region_coords[start_idx]}")
    print(f"End coord: {region_coords[end_idx]}")

    # Extract path between indices
    if start_idx <= end_idx:
        path1 = region_coords[start_idx:end_idx + 1]
        path2 = region_coords[end_idx:] + region_coords[:start_idx + 1]
        path2.reverse()
    else:
        path1 = region_coords[start_idx:] + region_coords[:end_idx + 1]
        path2 = region_coords[end_idx:start_idx + 1]
        path2.reverse()

    # Return the shorter path
    if len(path1) <= len(path2):
        print(f"Using path1 with {len(path1)} points")
        return path1
    else:
        print(f"Using path2 with {len(path2)} points")
        return path2

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import BASE_PATH

# Load the GeoJSON file
print("Loading GeoJSON file...")
input_file = os.path.join(BASE_PATH, 'using_data', 'boundaries_KR_20220407_updated.geojson')
with open(input_file, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

print("GeoJSON file loaded successfully\n")

# Extract all coordinates for both regions
print("Extracting Gangwon-do coordinates...")
gangwon_coords = extract_polygon_coordinates('강원도', geojson_data)
print(f"Found {len(gangwon_coords)} coordinates in Gangwon-do boundary\n")

print("Extracting Gyeonggi-do coordinates...")
gyeonggi_coords = extract_polygon_coordinates('경기도', geojson_data)
print(f"Found {len(gyeonggi_coords)} coordinates in Gyeonggi-do boundary\n")

# Define the points
gangwon_start = (127.10985655717332, 38.24187307265859)
gangwon_end = (127.10927177309406, 38.25523662544603)

print("="*80)
print("Extracting Gangwon-do line segment...")
print("="*80)
gangwon_line = extract_line_between_points(gangwon_start, gangwon_end, gangwon_coords)
print()

# The provided line segment 1
provided_line_1 = [
    [127.10928396558234, 38.255307559255044],
    [127.1080732224562, 38.25832272491212],
    [127.1079694444739, 38.261161212471166],
    [127.10921478026017, 38.263293400518876],
    [127.1093471196503, 38.26578495104539],
    [127.1090953962244, 38.26735158047009],
    [127.10826746430627, 38.26814680770329],
    [127.10809529178682, 38.26840635779823],
    [127.10883707848772, 38.2691530687954],
    [127.11045342971033, 38.269804545703664]
]

# Extract Gyeonggi-do line
gyeonggi_start = (127.11045342971033, 38.269804545703664)
gyeonggi_end = (127.09600085329743, 38.281011480877766)

print("="*80)
print("Extracting Gyeonggi-do line segment...")
print("="*80)
gyeonggi_line = extract_line_between_points(gyeonggi_start, gyeonggi_end, gyeonggi_coords)
print()

# The provided line segment 2
provided_line_2 = [
    [127.09599464047483, 38.28101752283618],
    [127.0953946252302, 38.281006041339595],
    [127.09503518647927, 38.28108245770255],
    [127.09554189527313, 38.2824305074943],
    [127.09544454727762, 38.282471653969]
]

# Combine all segments
combined_coordinates = []
combined_coordinates.extend(gangwon_line)
combined_coordinates.extend(provided_line_1)
combined_coordinates.extend(gyeonggi_line)
combined_coordinates.extend(provided_line_2)

# Create the final GeoJSON
final_geojson = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "coordinates": combined_coordinates,
        "type": "LineString"
    }
}

# Save the result
output_file = os.path.join(BASE_PATH, 'output', 'connected_line_v2.geojson')
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(final_geojson, f, ensure_ascii=False, indent=2)

print("="*80)
print(f"Final GeoJSON saved to {output_file}")
print(f"Total coordinates in combined line: {len(combined_coordinates)}")
print(f"  - Gangwon line: {len(gangwon_line)} points")
print(f"  - Provided line 1: {len(provided_line_1)} points")
print(f"  - Gyeonggi line: {len(gyeonggi_line)} points")
print(f"  - Provided line 2: {len(provided_line_2)} points")
print("="*80)

# Print a compact version of the GeoJSON
print("\nFinal GeoJSON String (compact):")
print(json.dumps(final_geojson, ensure_ascii=False))
