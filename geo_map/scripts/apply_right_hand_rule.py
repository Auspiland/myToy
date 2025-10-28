import json
import sys
import os

def calculate_polygon_area(coords):
    """
    Calculate the signed area of a polygon using the shoelace formula.
    Positive area = counter-clockwise (CCW)
    Negative area = clockwise (CW)
    """
    if len(coords) < 3:
        return 0

    area = 0
    n = len(coords)

    for i in range(n):
        j = (i + 1) % n
        area += coords[i][0] * coords[j][1]
        area -= coords[j][0] * coords[i][1]

    return area / 2

def is_ring_closed(coords):
    """
    Check if a ring is closed (first and last coordinates are the same).
    """
    if len(coords) < 2:
        return False

    first = coords[0]
    last = coords[-1]

    return first[0] == last[0] and first[1] == last[1]

def ensure_ring_closed(coords):
    """
    Ensure a ring is closed by adding the first coordinate at the end if needed.
    Modifies the list in-place and returns it.
    """
    if not is_ring_closed(coords):
        print(f"    Closing unclosed ring (adding first point to end)")
        coords.append(coords[0])
    return coords

def apply_right_hand_rule(coords, is_outer_ring=True):
    """
    Apply the right-hand rule to a polygon ring.
    - First ensures the ring is closed (in-place)
    - Outer rings should be counter-clockwise (CCW) - positive area
    - Inner rings (holes) should be clockwise (CW) - negative area

    Modifies the list in-place and returns it.
    """
    # First, ensure the ring is closed (modifies in-place)
    ensure_ring_closed(coords)

    area = calculate_polygon_area(coords)

    # For outer rings: area should be positive (CCW)
    # For inner rings (holes): area should be negative (CW)
    if is_outer_ring:
        if area < 0:
            # Reverse to make it CCW
            print(f"    Reversing outer ring (area={area:.2f})")
            coords.reverse()
    else:
        if area > 0:
            # Reverse to make it CW
            print(f"    Reversing inner ring (area={area:.2f})")
            coords.reverse()

    return coords

def process_geometry(geometry, feature_index):
    """
    Process a geometry and apply right-hand rule to all rings.
    """
    geom_type = geometry['type']

    if geom_type == 'Polygon':
        print(f"  Feature {feature_index}: Processing Polygon with {len(geometry['coordinates'])} ring(s)")
        new_coords = []
        for ring_idx, ring in enumerate(geometry['coordinates']):
            is_outer = (ring_idx == 0)
            new_ring = apply_right_hand_rule(ring, is_outer_ring=is_outer)
            new_coords.append(new_ring)
        geometry['coordinates'] = new_coords

    elif geom_type == 'MultiPolygon':
        print(f"  Feature {feature_index}: Processing MultiPolygon with {len(geometry['coordinates'])} polygon(s)")
        new_coords = []
        for poly_idx, polygon in enumerate(geometry['coordinates']):
            print(f"    Polygon {poly_idx}: {len(polygon)} ring(s)")
            new_polygon = []
            for ring_idx, ring in enumerate(polygon):
                is_outer = (ring_idx == 0)
                new_ring = apply_right_hand_rule(ring, is_outer_ring=is_outer)
                new_polygon.append(new_ring)
            new_coords.append(new_polygon)
        geometry['coordinates'] = new_coords

    return geometry

def apply_right_hand_rule_to_geojson(input_file, output_file=None):
    """
    Read a GeoJSON file, apply right-hand rule to all polygons, and save.
    If output_file is None, overwrites the input file.
    """
    print(f"Loading GeoJSON file: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    print(f"Loaded GeoJSON with {len(geojson_data.get('features', []))} features\n")

    # Process each feature
    features_processed = 0
    for idx, feature in enumerate(geojson_data.get('features', [])):
        if 'geometry' in feature and feature['geometry']:
            geom_type = feature['geometry']['type']
            if geom_type in ['Polygon', 'MultiPolygon']:
                features_processed += 1
                feature['geometry'] = process_geometry(feature['geometry'], idx)

    print(f"\nProcessed {features_processed} polygon/multipolygon features")

    # Save the result
    if output_file is None:
        output_file = input_file

    print(f"\nSaving to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)

    print("Done!")

if __name__ == "__main__":
    # Add parent directory to sys.path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    sys.path.insert(0, parent_dir)

    from config import BASE_PATH

    # Default input file
    input_file = os.path.join(BASE_PATH, 'static', 'whole.geojson')

    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    output_file = input_file

    print("="*80)
    print("Right-Hand Rule Converter for GeoJSON")
    print("="*80)
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file} (in-place update)")
    print("="*80)
    print()

    apply_right_hand_rule_to_geojson(input_file, output_file)
