@echo off
REM Road Risk Pipeline - Local Execution Script
REM This script runs the entire pipeline locally for testing

echo ========================================
echo Road Risk Pipeline - Local Execution
echo ========================================

REM Set environment variables
set BASE_PATH=C:\Users\T3Q\jeonghan\DUMMY\Spark
set BRONZE_PATH=%BASE_PATH%\output\bronze
set SILVER_PATH=%BASE_PATH%\output\silver
set GOLD_PATH=%BASE_PATH%\output\gold
set INPUT_CSV=%BASE_PATH%\data\roads.csv
set LOOKUP_LOAD_GRADE_CSV=%BASE_PATH%\conf\load_grade_lookup.csv
set PARTITION_DT=20251103
set PYTHONPATH=%BASE_PATH%\spark_jobs

echo.
echo Configuration:
echo   BASE_PATH: %BASE_PATH%
echo   PARTITION_DT: %PARTITION_DT%
echo.

REM Create output directories
if not exist "%BASE_PATH%\output\bronze" mkdir "%BASE_PATH%\output\bronze"
if not exist "%BASE_PATH%\output\silver" mkdir "%BASE_PATH%\output\silver"
if not exist "%BASE_PATH%\output\gold" mkdir "%BASE_PATH%\output\gold"
if not exist "%BASE_PATH%\logs" mkdir "%BASE_PATH%\logs"

echo ========================================
echo Step 1: Bronze Layer - Ingest CSV
echo ========================================
cd /d "%BASE_PATH%\spark_jobs"
python 01_ingest_csv.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Bronze layer failed!
    exit /b 1
)

echo.
echo ========================================
echo Step 2: Silver Layer - Enrich Lookup
echo ========================================
python 02_enrich_lookup.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Silver layer failed!
    exit /b 1
)

echo.
echo ========================================
echo Step 3: Gold Layer - Compute Scores
echo ========================================
python 03_compute_scores.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Score computation failed!
    exit /b 1
)

echo.
echo ========================================
echo Step 4: Gold Layer - Compute Risk
echo ========================================
python 04_compute_risk.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Risk computation failed!
    exit /b 1
)

echo.
echo ========================================
echo Step 5: Gold Layer - Publish Aggregates
echo ========================================
python 05_publish_aggregates.py
if %ERRORLEVEL% neq 0 (
    echo ERROR: Aggregate publication failed!
    exit /b 1
)

echo.
echo ========================================
echo Pipeline completed successfully!
echo ========================================
echo.
echo Output locations:
echo   Bronze: %BRONZE_PATH%\dt=%PARTITION_DT%
echo   Silver: %SILVER_PATH%\dt=%PARTITION_DT%
echo   Gold:   %GOLD_PATH%\
echo.

cd /d "%BASE_PATH%"
pause
