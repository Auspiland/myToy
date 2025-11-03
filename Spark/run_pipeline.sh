#!/bin/bash
# Road Risk Pipeline - Local Execution Script
# This script runs the entire pipeline locally for testing

echo "========================================"
echo "Road Risk Pipeline - Local Execution"
echo "========================================"

# Set environment variables
export BASE_PATH="${BASE_PATH:-/opt/road}"
export BRONZE_PATH="${BRONZE_PATH:-$BASE_PATH/output/bronze}"
export SILVER_PATH="${SILVER_PATH:-$BASE_PATH/output/silver}"
export GOLD_PATH="${GOLD_PATH:-$BASE_PATH/output/gold}"
export INPUT_CSV="${INPUT_CSV:-$BASE_PATH/data/roads.csv}"
export LOOKUP_LOAD_GRADE_CSV="${LOOKUP_LOAD_GRADE_CSV:-$BASE_PATH/conf/load_grade_lookup.csv}"
export PARTITION_DT="${PARTITION_DT:-$(date +%Y%m%d)}"
export PYTHONPATH="$BASE_PATH/spark_jobs"

echo ""
echo "Configuration:"
echo "  BASE_PATH: $BASE_PATH"
echo "  PARTITION_DT: $PARTITION_DT"
echo ""

# Create output directories
mkdir -p "$BASE_PATH/output/bronze"
mkdir -p "$BASE_PATH/output/silver"
mkdir -p "$BASE_PATH/output/gold"
mkdir -p "$BASE_PATH/logs"

# Change to spark_jobs directory
cd "$BASE_PATH/spark_jobs" || exit 1

echo "========================================"
echo "Step 1: Bronze Layer - Ingest CSV"
echo "========================================"
python 01_ingest_csv.py
if [ $? -ne 0 ]; then
    echo "ERROR: Bronze layer failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "Step 2: Silver Layer - Enrich Lookup"
echo "========================================"
python 02_enrich_lookup.py
if [ $? -ne 0 ]; then
    echo "ERROR: Silver layer failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "Step 3: Gold Layer - Compute Scores"
echo "========================================"
python 03_compute_scores.py
if [ $? -ne 0 ]; then
    echo "ERROR: Score computation failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "Step 4: Gold Layer - Compute Risk"
echo "========================================"
python 04_compute_risk.py
if [ $? -ne 0 ]; then
    echo "ERROR: Risk computation failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "Step 5: Gold Layer - Publish Aggregates"
echo "========================================"
python 05_publish_aggregates.py
if [ $? -ne 0 ]; then
    echo "ERROR: Aggregate publication failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "Pipeline completed successfully!"
echo "========================================"
echo ""
echo "Output locations:"
echo "  Bronze: $BRONZE_PATH/dt=$PARTITION_DT"
echo "  Silver: $SILVER_PATH/dt=$PARTITION_DT"
echo "  Gold:   $GOLD_PATH/"
echo ""
