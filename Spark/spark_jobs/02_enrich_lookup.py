"""
SILVER Layer: Enrich with lookup tables and derive features

Purpose:
    - Join with load grade lookup (설계하중 → 톤수)
    - Map road type to required load capacity (요구하중)
    - Calculate derived features (경과연수)
    - Validate enriched data
"""
import sys
import time
from pyspark.sql import functions as F

sys.path.append('.')

from common import ConfigLoader, SparkFactory, get_logger, DataQualityValidator
from common.logger import MetricsLogger


def create_road_type_lookup(spark):
    """
    Create lookup table: 도로종류 → 요구하중 (톤)

    Business rules:
    - 고속국도: DB-24 equivalent (43.2 tons)
    - 국도/지방도: DB-18 equivalent (32.4 tons)
    - 기타: DB-13.5 equivalent (24.3 tons)
    """
    data = [
        ("고속국도", 43.2),
        ("국도", 32.4),
        ("지방도", 32.4),
        ("시도", 32.4),
        ("군도", 24.3),
        ("구도", 24.3),
        ("기타", 24.3),
    ]

    return spark.createDataFrame(data, schema="도로종류 string, 요구하중_ton double")


def normalize_design_load(df):
    """
    Normalize 설계하중 string column

    - Remove whitespace
    - Handle common variations
    """
    logger = get_logger(__name__)
    logger.info("Normalizing design load strings")

    # Remove all whitespace
    df = df.withColumn(
        "설계하중_norm",
        F.regexp_replace(F.col("설계하중"), r"\s+", "")
    )

    # Handle null/empty
    df = df.withColumn(
        "설계하중_norm",
        F.when(
            (F.col("설계하중_norm").isNull()) | (F.col("설계하중_norm") == ""),
            F.lit(None)
        ).otherwise(F.col("설계하중_norm"))
    )

    return df


def enrich_with_lookups(df, lookup_df, road_type_lookup):
    """
    Enrich Bronze data with lookup tables

    Args:
        df: Bronze DataFrame
        lookup_df: Load grade lookup (grade, db, tons)
        road_type_lookup: Road type to required load mapping
    """
    logger = get_logger(__name__)
    logger.info("Enriching with lookup tables")

    # Normalize design load
    df = normalize_design_load(df)

    # Prepare lookup table (normalize db column)
    lookup_normalized = lookup_df.withColumn(
        "db_key",
        F.regexp_replace(F.col("db"), r"\s+", "")
    )

    # Join with load grade lookup to get design load in tons
    logger.info("Joining with load grade lookup")
    df = (df
          .join(
        lookup_normalized.select("db_key", "tons"),
        df["설계하중_norm"] == lookup_normalized["db_key"],
        "left"
    )
          .withColumnRenamed("tons", "설계하중_ton"))

    # Join with road type lookup to get required load
    logger.info("Joining with road type lookup")
    df = df.join(road_type_lookup, "도로종류", "left")

    return df


def calculate_derived_features(df):
    """
    Calculate derived features

    Features:
    - 경과연수: Current year - 준공년도
    - 용량비율: 설계하중_ton / 요구하중_ton
    """
    logger = get_logger(__name__)
    logger.info("Calculating derived features")

    current_year = 2025

    # Calculate age
    df = df.withColumn(
        "경과연수",
        F.when(
            F.col("준공년도").isNotNull(),
            F.lit(current_year) - F.col("준공년도")
        ).otherwise(F.lit(None))
    )

    # Calculate capacity ratio
    df = df.withColumn(
        "용량비율",
        F.when(
            (F.col("설계하중_ton").isNotNull()) & (F.col("요구하중_ton").isNotNull()) &
            (F.col("요구하중_ton") > 0),
            F.col("설계하중_ton") / F.col("요구하중_ton")
        ).otherwise(F.lit(None))
    )

    return df


def validate_silver_data(df, validator):
    """Validate Silver layer data quality"""
    logger = get_logger(__name__)
    logger.info("Running Silver layer validations")

    validator.reset()

    # Basic validations
    validator.validate_not_empty(df, "Silver Data")

    # Check enrichment success rate
    total = df.count()
    with_design_load = df.filter(F.col("설계하중_ton").isNotNull()).count()
    with_required_load = df.filter(F.col("요구하중_ton").isNotNull()).count()
    with_age = df.filter(F.col("경과연수").isNotNull()).count()

    design_load_rate = with_design_load / total if total > 0 else 0
    required_load_rate = with_required_load / total if total > 0 else 0
    age_rate = with_age / total if total > 0 else 0

    logger.info(f"Design load enrichment rate: {design_load_rate:.2%}")
    logger.info(f"Required load enrichment rate: {required_load_rate:.2%}")
    logger.info(f"Age calculation rate: {age_rate:.2%}")

    # Validate enrichment rates are acceptable
    if design_load_rate < 0.3:
        logger.warning(f"Low design load enrichment rate: {design_load_rate:.2%}")

    if required_load_rate < 0.8:
        logger.warning(f"Low required load enrichment rate: {required_load_rate:.2%}")

    # Validate derived features
    if "경과연수" in df.columns:
        validator.validate_range(df, "경과연수", min_val=0, max_val=200, name="Silver Data")

    logger.info(validator.summary())

    return validator.all_passed()


def main():
    """Main execution function"""
    start_time = time.time()
    logger = get_logger(__name__)
    logger.info("=" * 80)
    logger.info("Starting Silver Layer Enrichment (02_enrich_lookup)")
    logger.info("=" * 80)

    spark = None

    try:
        # Load configuration
        config = ConfigLoader.from_env()
        bronze_path = config.get("bronze_path", config.get("BRONZE_PATH"))
        silver_path = config.get("silver_path", config.get("SILVER_PATH"))
        lookup_csv = config.get("lookup_load_grade_csv", config.get("LOOKUP_LOAD_GRADE_CSV"))
        partition_dt = config.get("partition_dt", config.get("PARTITION_DT", "20251103"))

        logger.info(f"Bronze Path: {bronze_path}")
        logger.info(f"Silver Path: {silver_path}")
        logger.info(f"Lookup CSV: {lookup_csv}")
        logger.info(f"Partition Date: {partition_dt}")

        # Create Spark session
        spark = SparkFactory.create_session("road_enrich_silver")
        metrics = MetricsLogger(logger)
        validator = DataQualityValidator(logger)

        # Read Bronze data
        bronze_input = f"{bronze_path}/dt={partition_dt}"
        logger.info(f"Reading Bronze data from: {bronze_input}")
        df = spark.read.parquet(bronze_input)
        metrics.log_dataframe_stats(df, "Bronze Input")

        # Read lookup table
        logger.info(f"Reading lookup table: {lookup_csv}")
        lookup_df = (spark.read
                     .option("header", "true")
                     .option("inferSchema", "true")
                     .csv(lookup_csv))

        logger.info(f"Lookup table rows: {lookup_df.count()}")

        # Create road type lookup
        road_type_lookup = create_road_type_lookup(spark)

        # Enrich with lookups
        df_enriched = enrich_with_lookups(df, lookup_df, road_type_lookup)
        metrics.log_dataframe_stats(df_enriched, "After Lookup Join")

        # Calculate derived features
        df_final = calculate_derived_features(df_enriched)
        metrics.log_dataframe_stats(df_final, "After Feature Engineering")
        metrics.log_null_stats(df_final, "After Feature Engineering")

        # Validate
        validation_passed = validate_silver_data(df_final, validator)

        if not validation_passed:
            logger.warning("Data quality validation failed, but proceeding with write")

        # Write to Silver layer
        output_path = f"{silver_path}/dt={partition_dt}"
        logger.info(f"Writing to Silver layer: {output_path}")

        (df_final
         .write
         .mode("overwrite")
         .option("compression", "snappy")
         .parquet(output_path))

        # Final metrics
        final_count = df_final.count()
        duration = time.time() - start_time
        metrics.log_processing_complete("Silver Enrichment", final_count, duration)

        logger.info("=" * 80)
        logger.info("Silver Layer Enrichment completed successfully")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"Silver enrichment failed: {str(e)}", exc_info=True)
        return 1

    finally:
        if spark:
            SparkFactory.stop_session(spark)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
