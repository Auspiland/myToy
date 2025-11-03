"""
BRONZE Layer: Ingest raw CSV data with validation and error handling

Purpose:
    - Load raw road infrastructure CSV data
    - Apply schema validation
    - Perform basic data quality checks
    - Write to Bronze layer (partitioned by date)
"""
import sys
import time
from pyspark.sql import types as T, functions as F

# Add common module to path
sys.path.append('.')

from common import ConfigLoader, SparkFactory, get_logger, DataQualityValidator
from common.logger import MetricsLogger


# Define schema for road infrastructure data
ROAD_SCHEMA = T.StructType([
    T.StructField("도로종류", T.StringType(), nullable=True),
    T.StructField("노선명", T.StringType(), nullable=True),
    T.StructField("시설명", T.StringType(), nullable=True),
    T.StructField("시도", T.StringType(), nullable=True),
    T.StructField("시군구", T.StringType(), nullable=True),
    T.StructField("읍면동", T.StringType(), nullable=True),
    T.StructField("리", T.StringType(), nullable=True),
    T.StructField("총길이", T.IntegerType(), nullable=True),
    T.StructField("총폭", T.DoubleType(), nullable=True),
    T.StructField("유효폭", T.DoubleType(), nullable=True),
    T.StructField("높이", T.DoubleType(), nullable=True),
    T.StructField("경간수", T.IntegerType(), nullable=True),
    T.StructField("최대경간장", T.DoubleType(), nullable=True),
    T.StructField("상부구조", T.StringType(), nullable=True),
    T.StructField("하부구조", T.StringType(), nullable=True),
    T.StructField("설계하중", T.StringType(), nullable=True),
    T.StructField("교통량", T.IntegerType(), nullable=True),
    T.StructField("기관구분1", T.StringType(), nullable=True),
    T.StructField("기관구분2", T.StringType(), nullable=True),
    T.StructField("기관구분3", T.StringType(), nullable=True),
    T.StructField("준공년도", T.IntegerType(), nullable=True),
])


def clean_bronze_data(df):
    """
    Apply minimal cleaning for Bronze layer

    Rules:
    - Fill missing 하부구조 with '미상'
    - Trim whitespace from string columns
    - Add ingestion timestamp
    """
    logger = get_logger(__name__)
    logger.info("Applying Bronze layer cleaning rules")

    # Trim string columns
    string_cols = [f.name for f in ROAD_SCHEMA.fields if isinstance(f.dataType, T.StringType)]
    for col in string_cols:
        df = df.withColumn(col, F.trim(F.col(col)))

    # Fill missing values
    df = df.fillna({"하부구조": "미상"})

    # Add metadata columns
    df = df.withColumn("ingestion_timestamp", F.current_timestamp())
    df = df.withColumn("source_file", F.input_file_name())

    return df


def validate_bronze_data(df, validator):
    """Validate Bronze layer data quality"""
    logger = get_logger(__name__)
    logger.info("Running Bronze layer validations")

    validator.reset()

    # Validate not empty
    validator.validate_not_empty(df, "Bronze Data")

    # Validate schema
    required_columns = [f.name for f in ROAD_SCHEMA.fields]
    validator.validate_schema(df, required_columns, "Bronze Data")

    # Validate critical columns have acceptable null ratios
    critical_columns = ["시설명", "시도", "준공년도"]
    validator.validate_null_threshold(df, critical_columns, max_null_ratio=0.5, name="Bronze Data")

    # Validate numeric ranges
    if "준공년도" in df.columns:
        validator.validate_range(df, "준공년도", min_val=1900, max_val=2025, name="Bronze Data")

    # Log summary
    logger.info(validator.summary())

    return validator.all_passed()


def main():
    """Main execution function"""
    start_time = time.time()
    logger = get_logger(__name__)
    logger.info("=" * 80)
    logger.info("Starting Bronze Layer Ingestion (01_ingest_csv)")
    logger.info("=" * 80)

    spark = None

    try:
        # Load configuration
        config = ConfigLoader.from_env()
        input_csv = config.get("input_csv", config.get("INPUT_CSV"))
        bronze_path = config.get("bronze_path", config.get("BRONZE_PATH"))
        partition_dt = config.get("partition_dt", config.get("PARTITION_DT", "20251103"))

        logger.info(f"Input CSV: {input_csv}")
        logger.info(f"Bronze Path: {bronze_path}")
        logger.info(f"Partition Date: {partition_dt}")

        # Create Spark session
        spark = SparkFactory.create_session("road_ingest_bronze")
        metrics = MetricsLogger(logger)
        validator = DataQualityValidator(logger)

        # Read CSV with schema
        logger.info("Reading CSV file...")
        df = (spark.read
              .option("header", "true")
              .option("mode", "PERMISSIVE")
              .option("encoding", "UTF-8")
              .schema(ROAD_SCHEMA)
              .csv(input_csv))

        metrics.log_dataframe_stats(df, "Raw Input")

        # Apply cleaning
        df_cleaned = clean_bronze_data(df)
        metrics.log_dataframe_stats(df_cleaned, "After Cleaning")
        metrics.log_null_stats(df_cleaned, "After Cleaning")

        # Validate data quality
        validation_passed = validate_bronze_data(df_cleaned, validator)

        if not validation_passed:
            logger.warning("Data quality validation failed, but proceeding with write")

        # Write to Bronze layer
        output_path = f"{bronze_path}/dt={partition_dt}"
        logger.info(f"Writing to Bronze layer: {output_path}")

        (df_cleaned
         .write
         .mode("overwrite")
         .option("compression", "snappy")
         .parquet(output_path))

        # Final metrics
        final_count = df_cleaned.count()
        duration = time.time() - start_time
        metrics.log_processing_complete("Bronze Ingestion", final_count, duration)

        logger.info("=" * 80)
        logger.info("Bronze Layer Ingestion completed successfully")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"Bronze ingestion failed: {str(e)}", exc_info=True)
        return 1

    finally:
        if spark:
            SparkFactory.stop_session(spark)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
