"""
GOLD Layer: Compute component risk scores

Purpose:
    - Calculate individual risk component scores (0-1 scale)
    - Components: Capacity, Age, Traffic, Span, Width, Metadata
    - Handle missing values with appropriate defaults
"""
import sys
import time
from pyspark.sql import functions as F

sys.path.append('.')

from common import ConfigLoader, SparkFactory, get_logger, DataQualityValidator
from common.logger import MetricsLogger


def compute_capacity_score(df):
    """
    S_용량: Capacity deficiency score

    Logic:
    - Score = max(0, 1 - (설계하중_ton / 요구하중_ton))
    - Higher score = greater deficiency (worse)
    - Missing values = 0.5 (medium risk)
    """
    return F.when(
        F.col("요구하중_ton").isNull() | F.col("설계하중_ton").isNull() |
        (F.col("요구하중_ton") <= 0),
        F.lit(0.5)
    ).otherwise(
        F.greatest(
            F.lit(0.0),
            F.lit(1.0) - (F.col("설계하중_ton") / F.col("요구하중_ton"))
        )
    )


def compute_age_score(df):
    """
    S_노후: Age/deterioration score

    Logic:
    - Normalize age to 0-1 scale (max 50 years)
    - Score = min(1.0, 경과연수 / 50)
    - Missing values = 0.5 (medium risk)
    """
    return F.when(
        F.col("경과연수").isNull() | (F.col("경과연수") < 0),
        F.lit(0.5)
    ).otherwise(
        F.least(
            F.lit(1.0),
            F.col("경과연수") / F.lit(50.0)
        )
    )


def compute_traffic_score(df):
    """
    S_교통: Traffic load score

    Logic:
    - Normalize traffic to 0-1 scale (max 40,000 vehicles/day)
    - Score = min(1.0, 교통량 / 40000)
    - Missing values = 0.5 (medium risk)
    """
    return F.when(
        F.col("교통량").isNull() | (F.col("교통량") < 0),
        F.lit(0.5)
    ).otherwise(
        F.least(
            F.lit(1.0),
            F.col("교통량") / F.lit(40000.0)
        )
    )


def compute_span_score(df):
    """
    S_경간: Span length score

    Logic:
    - Normalize span to 0-1 scale (max 80m)
    - Score = min(1.0, 최대경간장 / 80)
    - Longer spans = higher structural risk
    - Missing values = 0.5 (medium risk)
    """
    return F.when(
        F.col("최대경간장").isNull() | (F.col("최대경간장") < 0),
        F.lit(0.5)
    ).otherwise(
        F.least(
            F.lit(1.0),
            F.col("최대경간장") / F.lit(80.0)
        )
    )


def compute_width_score(df):
    """
    S_폭: Width utilization score

    Logic:
    - Score = max(0, 1 - (유효폭 / 총폭))
    - Lower utilization = higher risk
    - Missing values = 0.3 (low-medium risk)
    """
    return F.when(
        F.col("총폭").isNull() | F.col("유효폭").isNull() |
        (F.col("총폭") <= 0),
        F.lit(0.3)
    ).otherwise(
        F.greatest(
            F.lit(0.0),
            F.lit(1.0) - (F.col("유효폭") / F.col("총폭"))
        )
    )


def compute_metadata_score(df):
    """
    S_메타: Metadata completeness score

    Logic:
    - Penalize missing structural information
    - Missing 상부구조 or 하부구조 or 하부구조='미상' = 0.3
    - Complete metadata = 0.0 (no risk)
    """
    return F.when(
        F.col("상부구조").isNull() |
        F.col("하부구조").isNull() |
        (F.col("하부구조") == "미상"),
        F.lit(0.3)
    ).otherwise(
        F.lit(0.0)
    )


def compute_all_scores(df):
    """
    Compute all component risk scores

    Returns DataFrame with additional score columns
    """
    logger = get_logger(__name__)
    logger.info("Computing component risk scores")

    df = (df
          .withColumn("S_용량", compute_capacity_score(df))
          .withColumn("S_노후", compute_age_score(df))
          .withColumn("S_교통", compute_traffic_score(df))
          .withColumn("S_경간", compute_span_score(df))
          .withColumn("S_폭", compute_width_score(df))
          .withColumn("S_메타", compute_metadata_score(df)))

    return df


def validate_scores(df, validator):
    """Validate computed scores"""
    logger = get_logger(__name__)
    logger.info("Running score validation")

    validator.reset()

    # Validate not empty
    validator.validate_not_empty(df, "Score Data")

    # Validate score ranges (all should be 0-1)
    score_columns = ["S_용량", "S_노후", "S_교통", "S_경간", "S_폭", "S_메타"]
    for col in score_columns:
        validator.validate_range(df, col, min_val=0.0, max_val=1.0, name="Scores")

    # Check for nulls in scores (should be none)
    null_counts = []
    for col in score_columns:
        null_count = df.filter(F.col(col).isNull()).count()
        if null_count > 0:
            null_counts.append((col, null_count))
            logger.warning(f"Found {null_count} nulls in {col}")

    logger.info(validator.summary())

    return validator.all_passed() and len(null_counts) == 0


def main():
    """Main execution function"""
    start_time = time.time()
    logger = get_logger(__name__)
    logger.info("=" * 80)
    logger.info("Starting Score Computation (03_compute_scores)")
    logger.info("=" * 80)

    spark = None

    try:
        # Load configuration
        config = ConfigLoader.from_env()
        silver_path = config.get("silver_path", config.get("SILVER_PATH"))
        gold_path = config.get("gold_path", config.get("GOLD_PATH"))
        partition_dt = config.get("partition_dt", config.get("PARTITION_DT", "20251103"))

        logger.info(f"Silver Path: {silver_path}")
        logger.info(f"Gold Path: {gold_path}")
        logger.info(f"Partition Date: {partition_dt}")

        # Create Spark session
        spark = SparkFactory.create_session("road_scores")
        metrics = MetricsLogger(logger)
        validator = DataQualityValidator(logger)

        # Read Silver data
        silver_input = f"{silver_path}/dt={partition_dt}"
        logger.info(f"Reading Silver data from: {silver_input}")
        df = spark.read.parquet(silver_input)
        metrics.log_dataframe_stats(df, "Silver Input")

        # Compute scores
        df_with_scores = compute_all_scores(df)
        metrics.log_dataframe_stats(df_with_scores, "After Score Computation")

        # Log score statistics
        score_cols = ["S_용량", "S_노후", "S_교통", "S_경간", "S_폭", "S_메타"]
        logger.info("Score Statistics:")
        stats = df_with_scores.select([
            F.avg(col).alias(f"{col}_avg")
            for col in score_cols
        ]).collect()[0]

        for col in score_cols:
            avg_val = stats[f"{col}_avg"]
            logger.info(f"  {col}: avg={avg_val:.3f}")

        # Validate
        validation_passed = validate_scores(df_with_scores, validator)

        if not validation_passed:
            logger.error("Score validation failed!")
            return 1

        # Write to Gold layer
        output_path = f"{gold_path}/scores/dt={partition_dt}"
        logger.info(f"Writing to Gold layer: {output_path}")

        (df_with_scores
         .write
         .mode("overwrite")
         .option("compression", "snappy")
         .parquet(output_path))

        # Final metrics
        final_count = df_with_scores.count()
        duration = time.time() - start_time
        metrics.log_processing_complete("Score Computation", final_count, duration)

        logger.info("=" * 80)
        logger.info("Score Computation completed successfully")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"Score computation failed: {str(e)}", exc_info=True)
        return 1

    finally:
        if spark:
            SparkFactory.stop_session(spark)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
