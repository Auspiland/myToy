"""
GOLD Layer: Compute overall risk score and level

Purpose:
    - Calculate weighted risk score from components
    - Assign risk levels (높음, 보통, 낮음)
    - Validate risk distribution
"""
import sys
import time
from pyspark.sql import functions as F

sys.path.append('.')

from common import ConfigLoader, SparkFactory, get_logger, DataQualityValidator
from common.logger import MetricsLogger


# Risk weights (must sum to 1.0)
RISK_WEIGHTS = {
    "S_용량": 0.35,  # Capacity deficiency - most critical
    "S_노후": 0.25,  # Age/deterioration
    "S_교통": 0.20,  # Traffic load
    "S_경간": 0.10,  # Span length
    "S_폭": 0.05,    # Width utilization
    "S_메타": 0.05,  # Metadata completeness
}

# Risk level thresholds
RISK_THRESHOLDS = {
    "높음": 0.6,   # High risk: >= 0.6
    "보통": 0.3,   # Medium risk: 0.3 <= score < 0.6
    # 낮음: < 0.3  # Low risk: < 0.3
}


def compute_weighted_risk(df):
    """
    Compute weighted risk score

    Formula:
    RISK = Σ(weight_i × score_i)

    Returns DataFrame with RISK column
    """
    logger = get_logger(__name__)
    logger.info("Computing weighted risk score")
    logger.info(f"Weights: {RISK_WEIGHTS}")

    # Validate weights sum to 1.0
    weight_sum = sum(RISK_WEIGHTS.values())
    if abs(weight_sum - 1.0) > 0.001:
        logger.warning(f"Weights sum to {weight_sum:.3f}, not 1.0")

    # Compute weighted sum
    risk_expr = sum(
        F.lit(weight) * F.col(score_col)
        for score_col, weight in RISK_WEIGHTS.items()
    )

    df = df.withColumn("RISK", F.round(risk_expr, 3))

    return df


def assign_risk_level(df):
    """
    Assign risk level based on thresholds

    Levels:
    - 높음 (High): RISK >= 0.6
    - 보통 (Medium): 0.3 <= RISK < 0.6
    - 낮음 (Low): RISK < 0.3
    """
    logger = get_logger(__name__)
    logger.info("Assigning risk levels")
    logger.info(f"Thresholds: {RISK_THRESHOLDS}")

    df = df.withColumn(
        "RISK_LEVEL",
        F.when(F.col("RISK") >= RISK_THRESHOLDS["높음"], F.lit("높음"))
        .when(F.col("RISK") >= RISK_THRESHOLDS["보통"], F.lit("보통"))
        .otherwise(F.lit("낮음"))
    )

    return df


def validate_risk_data(df, validator):
    """Validate risk data"""
    logger = get_logger(__name__)
    logger.info("Running risk validation")

    validator.reset()

    # Validate not empty
    validator.validate_not_empty(df, "Risk Data")

    # Validate RISK range
    validator.validate_range(df, "RISK", min_val=0.0, max_val=1.0, name="Risk Data")

    # Check for nulls
    null_count = df.filter(F.col("RISK").isNull()).count()
    if null_count > 0:
        logger.error(f"Found {null_count} null RISK values!")
        return False

    # Validate RISK_LEVEL values
    valid_levels = {"높음", "보통", "낮음"}
    level_counts = (df.groupBy("RISK_LEVEL")
                    .count()
                    .collect())

    logger.info("Risk level distribution:")
    for row in level_counts:
        level = row["RISK_LEVEL"]
        count = row["count"]
        logger.info(f"  {level}: {count:,}")

        if level not in valid_levels:
            logger.error(f"Invalid risk level found: {level}")
            return False

    logger.info(validator.summary())

    return validator.all_passed()


def log_risk_statistics(df, logger):
    """Log detailed risk statistics"""
    logger.info("=" * 60)
    logger.info("Risk Statistics Summary")
    logger.info("=" * 60)

    # Overall statistics
    stats = df.select(
        F.min("RISK").alias("min_risk"),
        F.max("RISK").alias("max_risk"),
        F.avg("RISK").alias("avg_risk"),
        F.expr("percentile_approx(RISK, 0.5)").alias("median_risk"),
        F.expr("percentile_approx(RISK, 0.9)").alias("p90_risk"),
    ).collect()[0]

    logger.info(f"Min Risk:     {stats['min_risk']:.3f}")
    logger.info(f"Max Risk:     {stats['max_risk']:.3f}")
    logger.info(f"Average Risk: {stats['avg_risk']:.3f}")
    logger.info(f"Median Risk:  {stats['median_risk']:.3f}")
    logger.info(f"P90 Risk:     {stats['p90_risk']:.3f}")

    # Risk level distribution
    total = df.count()
    level_dist = df.groupBy("RISK_LEVEL").count().collect()

    logger.info("\nRisk Level Distribution:")
    for row in sorted(level_dist, key=lambda x: x["count"], reverse=True):
        level = row["RISK_LEVEL"]
        count = row["count"]
        pct = count / total * 100
        logger.info(f"  {level}: {count:,} ({pct:.1f}%)")

    logger.info("=" * 60)


def main():
    """Main execution function"""
    start_time = time.time()
    logger = get_logger(__name__)
    logger.info("=" * 80)
    logger.info("Starting Risk Computation (04_compute_risk)")
    logger.info("=" * 80)

    spark = None

    try:
        # Load configuration
        config = ConfigLoader.from_env()
        gold_path = config.get("gold_path", config.get("GOLD_PATH"))
        partition_dt = config.get("partition_dt", config.get("PARTITION_DT", "20251103"))

        logger.info(f"Gold Path: {gold_path}")
        logger.info(f"Partition Date: {partition_dt}")

        # Create Spark session
        spark = SparkFactory.create_session("road_risk")
        metrics = MetricsLogger(logger)
        validator = DataQualityValidator(logger)

        # Read scores data
        scores_input = f"{gold_path}/scores/dt={partition_dt}"
        logger.info(f"Reading scores data from: {scores_input}")
        df = spark.read.parquet(scores_input)
        metrics.log_dataframe_stats(df, "Scores Input")

        # Compute weighted risk
        df_with_risk = compute_weighted_risk(df)

        # Assign risk levels
        df_final = assign_risk_level(df_with_risk)
        metrics.log_dataframe_stats(df_final, "After Risk Computation")

        # Log statistics
        log_risk_statistics(df_final, logger)

        # Validate
        validation_passed = validate_risk_data(df_final, validator)

        if not validation_passed:
            logger.error("Risk validation failed!")
            return 1

        # Write to Gold layer
        output_path = f"{gold_path}/risk/dt={partition_dt}"
        logger.info(f"Writing to Gold layer: {output_path}")

        (df_final
         .write
         .mode("overwrite")
         .option("compression", "snappy")
         .parquet(output_path))

        # Final metrics
        final_count = df_final.count()
        duration = time.time() - start_time
        metrics.log_processing_complete("Risk Computation", final_count, duration)

        logger.info("=" * 80)
        logger.info("Risk Computation completed successfully")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"Risk computation failed: {str(e)}", exc_info=True)
        return 1

    finally:
        if spark:
            SparkFactory.stop_session(spark)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
