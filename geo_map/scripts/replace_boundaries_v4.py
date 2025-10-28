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

def get_largest_polygon_index(geometry):
    """Find the index of the largest polygon in a MultiPolygon"""
    if geometry['type'] == 'Polygon':
        return None  # Single polygon, no index needed

    max_points = 0
    max_idx = 0
    for idx, polygon in enumerate(geometry['coordinates']):
        total_points = sum(len(ring) for ring in polygon)
        if total_points > max_points:
            max_points = total_points
            max_idx = idx

    return max_idx

def replace_boundary_section(coords: List[List[float]],
                             start_point: Tuple[float, float],
                             end_point: Tuple[float, float],
                             replacement_line: List[List[float]]) -> List[List[float]]:
    """
    Replace a section of polygon boundary between start and end points with the replacement line.
    The rest of the boundary is preserved.
    Always replaces the SHORTER path between start and end.
    """
    start_idx = find_closest_point_index(start_point, coords)
    end_idx = find_closest_point_index(end_point, coords)

    print(f"  Start index: {start_idx}, coord: {coords[start_idx]}")
    print(f"  End index: {end_idx}, coord: {coords[end_idx]}")
    print(f"  Original boundary: {len(coords)} points")

    # Calculate distances for both paths
    if start_idx <= end_idx:
        path1_length = end_idx - start_idx + 1  # Direct path
        path2_length = (len(coords) - end_idx) + start_idx  # Wrap-around path
    else:
        path1_length = (len(coords) - start_idx) + end_idx + 1  # Wrap-around path
        path2_length = start_idx - end_idx  # Direct path (backwards)

    print(f"  Path1 length: {path1_length}, Path2 length: {path2_length}")

    # Choose the shorter path to replace
    if start_idx <= end_idx:
        if path1_length <= path2_length:
            # Replace direct path: start → end
            new_coords = coords[:start_idx] + replacement_line + coords[end_idx + 1:]
            replaced_count = path1_length
        else:
            # Replace wrap-around path: keep start → end, replace the rest
            new_coords = coords[end_idx + 1:start_idx] + replacement_line
            replaced_count = path2_length
    else:
        if path1_length <= path2_length:
            # Replace wrap-around path: start → end (wrapping)
            new_coords = coords[end_idx + 1:start_idx] + replacement_line
            replaced_count = path1_length
        else:
            # Replace backwards path: keep wrap-around, replace middle
            new_coords = coords[:end_idx + 1] + replacement_line + coords[start_idx:]
            replaced_count = path2_length

    print(f"  New boundary: {len(new_coords)} points")
    print(f"  Replaced {replaced_count} points with {len(replacement_line)} points")

    return new_coords

def remove_small_polygons_near_boundary(geometry, center_point: Tuple[float, float], radius: float = 0.05):
    """
    Remove small polygons near a specific boundary point.
    """
    if geometry['type'] != 'MultiPolygon':
        return geometry

    removed_count = 0
    new_polygons = []

    for idx, polygon in enumerate(geometry['coordinates']):
        # Check if this polygon is near the center point
        outer_ring = polygon[0]
        is_near = False

        for coord in outer_ring:
            if distance(center_point, tuple(coord)) < radius:
                is_near = True
                break

        # Keep large polygons or polygons far from the boundary
        total_points = sum(len(ring) for ring in polygon)
        if total_points > 1000 or not is_near:
            new_polygons.append(polygon)
        else:
            removed_count += 1
            print(f"  Removed small polygon {idx} with {total_points} points")

    geometry['coordinates'] = new_polygons
    print(f"  Total removed: {removed_count} small polygons")
    return geometry

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import BASE_PATH

# Load the original GeoJSON file
print("Loading original GeoJSON file...")
input_file = os.path.join(BASE_PATH, 'using_data', 'boundaries_KR_20220407_updated.geojson')
with open(input_file, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)
print("Original GeoJSON loaded\n")

# Load the generated connected line
print("Loading generated connected line...")
connected_line_file = os.path.join(BASE_PATH, 'output', 'connected_line_v2.geojson')
with open(connected_line_file, 'r', encoding='utf-8') as f:
    connected_line_data = json.load(f)
connected_line = connected_line_data['geometry']['coordinates']
print(f"Connected line has {len(connected_line)} points\n")

# The replacement line is the ENTIRE connected line
replacement_line = connected_line
line_start = tuple(connected_line[0])
line_end = tuple(connected_line[-1])

print("="*80)
print("Replacement line:")
print("="*80)
print(f"Total points: {len(replacement_line)}")
print(f"Start point: {line_start}")
print(f"End point: {line_end}")
print()

# Find and modify Gangwon-do boundary
print("="*80)
print("Processing Gangwon-do boundary...")
print("="*80)
gangwon_found = False
for feature_idx, feature in enumerate(geojson_data['features']):
    props = feature['properties']
    # Check for Korean property names
    if any(value == '강원도' or value == '강원특별자치도' for value in props.values()):
        print(f"Found Gangwon-do feature: {props}")
        geometry = feature['geometry']

        if geometry['type'] == 'MultiPolygon':
            # Find the largest polygon
            largest_idx = get_largest_polygon_index(geometry)
            print(f"Largest polygon index: {largest_idx}")

            polygon = geometry['coordinates'][largest_idx]
            # Process only the outer ring (index 0)
            outer_ring = polygon[0]

            new_ring = replace_boundary_section(outer_ring, line_start, line_end, replacement_line)
            geojson_data['features'][feature_idx]['geometry']['coordinates'][largest_idx][0] = new_ring
            gangwon_found = True

        elif geometry['type'] == 'Polygon':
            # Process only the outer ring (index 0)
            outer_ring = geometry['coordinates'][0]
            new_ring = replace_boundary_section(outer_ring, line_start, line_end, replacement_line)
            geojson_data['features'][feature_idx]['geometry']['coordinates'][0] = new_ring
            gangwon_found = True

        break

if not gangwon_found:
    print("WARNING: Gangwon-do boundary not found or not modified!")

print()

# Find and modify Gyeonggi-do boundary
print("="*80)
print("Processing Gyeonggi-do boundary...")
print("="*80)
gyeonggi_found = False
for feature_idx, feature in enumerate(geojson_data['features']):
    props = feature['properties']
    # Check for Korean property names
    if any(value == '경기도' for value in props.values()):
        print(f"Found Gyeonggi-do feature: {props}")
        geometry = feature['geometry']

        if geometry['type'] == 'MultiPolygon':
            # Find the largest polygon BEFORE removing small ones
            largest_idx = get_largest_polygon_index(geometry)
            print(f"Largest polygon index: {largest_idx}")

            polygon = geometry['coordinates'][largest_idx]
            # Process only the outer ring (index 0)
            outer_ring = polygon[0]

            # Check if we need to reverse the replacement line
            # by checking which direction the polygon traverses
            start_idx_temp = find_closest_point_index(line_start, outer_ring)
            end_idx_temp = find_closest_point_index(line_end, outer_ring)

            # If start > end, the polygon goes in opposite direction
            # So we need to reverse the replacement line
            if start_idx_temp > end_idx_temp:
                print("  Reversing replacement line for Gyeonggi (opposite traversal direction)")
                replacement_line_gyeonggi = list(reversed(replacement_line))
                new_ring = replace_boundary_section(outer_ring, line_end, line_start, replacement_line_gyeonggi)
            else:
                new_ring = replace_boundary_section(outer_ring, line_start, line_end, replacement_line)

            geojson_data['features'][feature_idx]['geometry']['coordinates'][largest_idx][0] = new_ring

            # Remove inner rings (holes) near the boundary
            print("Removing inner rings (holes) near boundary...")
            boundary_center = ((line_start[0] + line_end[0]) / 2, (line_start[1] + line_end[1]) / 2)
            polygon_with_holes = geojson_data['features'][feature_idx]['geometry']['coordinates'][largest_idx]

            if len(polygon_with_holes) > 1:
                new_rings = [polygon_with_holes[0]]  # Keep outer ring
                removed_holes = 0

                for ring_idx in range(1, len(polygon_with_holes)):
                    inner_ring = polygon_with_holes[ring_idx]
                    is_near = False

                    for coord in inner_ring:
                        if distance(boundary_center, tuple(coord)) < 0.05:
                            is_near = True
                            break

                    if is_near:
                        removed_holes += 1
                        print(f"  Removed inner ring {ring_idx} with {len(inner_ring)} points")
                    else:
                        new_rings.append(inner_ring)

                geojson_data['features'][feature_idx]['geometry']['coordinates'][largest_idx] = new_rings
                print(f"  Total removed: {removed_holes} inner rings")

            # Now remove small polygons near the boundary
            print("Removing small polygons near boundary...")
            geojson_data['features'][feature_idx]['geometry'] = remove_small_polygons_near_boundary(
                geojson_data['features'][feature_idx]['geometry'], boundary_center, radius=0.05)

            gyeonggi_found = True

        elif geometry['type'] == 'Polygon':
            # Process only the outer ring (index 0)
            outer_ring = geometry['coordinates'][0]
            new_ring = replace_boundary_section(outer_ring, line_start, line_end, replacement_line)
            geojson_data['features'][feature_idx]['geometry']['coordinates'][0] = new_ring
            gyeonggi_found = True

        break

if not gyeonggi_found:
    print("WARNING: Gyeonggi-do boundary not found or not modified!")

print()

# Save the modified GeoJSON
output_file = os.path.join(BASE_PATH, 'using_data', 'boundaries_KR_20220407_modified.geojson')
print("="*80)
print(f"Saving modified GeoJSON to {output_file}...")
print("="*80)
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=2)

print("Modified GeoJSON saved successfully!")
if gangwon_found and gyeonggi_found:
    print("Both Gangwon-do and Gyeonggi-do boundaries have been updated")
elif gangwon_found:
    print("Only Gangwon-do boundary has been updated")
elif gyeonggi_found:
    print("Only Gyeonggi-do boundary has been updated")
else:
    print("No boundaries were updated!")
