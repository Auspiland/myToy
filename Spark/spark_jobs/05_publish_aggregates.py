"""
GOLD Layer: Publish aggregates and reports

Purpose:
    - Create regional aggregations (by 시도, 시군구)
    - Create route-level aggregations (by 노선명)
    - Create high-risk facility reports
    - Generate summary statistics
"""
import sys
import time
from pyspark.sql import functions as F, Window

sys.path.append('.')

from common import ConfigLoader, SparkFactory, get_logger, DataQualityValidator
from common.logger import MetricsLogger


def aggregate_by_region(df):
    """
    Aggregate by region (시도, 시군구, RISK_LEVEL)

    Returns:
        DataFrame with columns: 시도, 시군구, RISK_LEVEL, 시설수
    """
    logger = get_logger(__name__)
    logger.info("Aggregating by region")

    agg_df = (df
              .groupBy("시도", "시군구", "RISK_LEVEL")
              .agg(F.count("*").alias("시설수"))
              .orderBy("시도", "시군구", "RISK_LEVEL"))

    return agg_df


def aggregate_by_route(df):
    """
    Aggregate by route (노선명)

    Returns:
        DataFrame with columns: 노선명, avg_risk, 시설수, 높음, 보통, 낮음
    """
    logger = get_logger(__name__)
    logger.info("Aggregating by route")

    # Pivot risk levels
    agg_df = (df
              .groupBy("노선명")
              .agg(
        F.avg("RISK").alias("avg_risk"),
        F.count("*").alias("시설수"),
        F.sum(F.when(F.col("RISK_LEVEL") == "높음", 1).otherwise(0)).alias("높음"),
        F.sum(F.when(F.col("RISK_LEVEL") == "보통", 1).otherwise(0)).alias("보통"),
        F.sum(F.when(F.col("RISK_LEVEL") == "낮음", 1).otherwise(0)).alias("낮음"),
    )
              .orderBy(F.desc("avg_risk")))

    return agg_df


def create_high_risk_report(df):
    """
    Create report of high-risk facilities

    Returns top high-risk facilities with key attributes
    """
    logger = get_logger(__name__)
    logger.info("Creating high-risk facility report")

    high_risk = (df
                 .filter(F.col("RISK_LEVEL") == "높음")
                 .select(
        "시설명", "노선명", "시도", "시군구",
        "RISK", "RISK_LEVEL",
        "설계하중_ton", "요구하중_ton", "경과연수", "교통량",
        "S_용량", "S_노후", "S_교통"
    )
                 .orderBy(F.desc("RISK")))

    return high_risk


def create_summary_statistics(df):
    """
    Create overall summary statistics

    Returns single-row DataFrame with key metrics
    """
    logger = get_logger(__name__)
    logger.info("Creating summary statistics")

    summary = df.select(
        F.count("*").alias("total_facilities"),
        F.sum(F.when(F.col("RISK_LEVEL") == "높음", 1).otherwise(0)).alias("high_risk_count"),
        F.sum(F.when(F.col("RISK_LEVEL") == "보통", 1).otherwise(0)).alias("medium_risk_count"),
        F.sum(F.when(F.col("RISK_LEVEL") == "낮음", 1).otherwise(0)).alias("low_risk_count"),
        F.avg("RISK").alias("avg_risk"),
        F.max("RISK").alias("max_risk"),
        F.expr("percentile_approx(RISK, 0.9)").alias("p90_risk"),
        F.countDistinct("시도").alias("regions_count"),
        F.countDistinct("노선명").alias("routes_count"),
    )

    return summary


def aggregate_by_age_group(df):
    """
    Aggregate by age groups

    Age groups: 0-10, 10-20, 20-30, 30-40, 40-50, 50+
    """
    logger = get_logger(__name__)
    logger.info("Aggregating by age group")

    df_with_age_group = df.withColumn(
        "age_group",
        F.when(F.col("경과연수").isNull(), "미상")
        .when(F.col("경과연수") < 10, "0-10년")
        .when(F.col("경과연수") < 20, "10-20년")
        .when(F.col("경과연수") < 30, "20-30년")
        .when(F.col("경과연수") < 40, "30-40년")
        .when(F.col("경과연수") < 50, "40-50년")
        .otherwise("50년 이상")
    )

    agg_df = (df_with_age_group
              .groupBy("age_group")
              .agg(
        F.count("*").alias("시설수"),
        F.avg("RISK").alias("avg_risk"),
        F.sum(F.when(F.col("RISK_LEVEL") == "높음", 1).otherwise(0)).alias("높음"),
        F.sum(F.when(F.col("RISK_LEVEL") == "보통", 1).otherwise(0)).alias("보통"),
        F.sum(F.when(F.col("RISK_LEVEL") == "낮음", 1).otherwise(0)).alias("낮음"),
    )
              .orderBy("age_group"))

    return agg_df


def validate_aggregates(df_region, df_route, df_summary, validator):
    """Validate aggregate data quality"""
    logger = get_logger(__name__)
    logger.info("Running aggregate validation")

    validator.reset()

    # Validate all aggregates are not empty
    validator.validate_not_empty(df_region, "Region Aggregates")
    validator.validate_not_empty(df_route, "Route Aggregates")
    validator.validate_not_empty(df_summary, "Summary Statistics")

    logger.info(validator.summary())

    return validator.all_passed()


def main():
    """Main execution function"""
    start_time = time.time()
    logger = get_logger(__name__)
    logger.info("=" * 80)
    logger.info("Starting Aggregate Publication (05_publish_aggregates)")
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
        spark = SparkFactory.create_session("road_publish")
        metrics = MetricsLogger(logger)
        validator = DataQualityValidator(logger)

        # Read risk data
        risk_input = f"{gold_path}/risk/dt={partition_dt}"
        logger.info(f"Reading risk data from: {risk_input}")
        df = spark.read.parquet(risk_input)
        metrics.log_dataframe_stats(df, "Risk Input")

        # Create aggregations
        logger.info("Creating aggregations...")

        df_region = aggregate_by_region(df)
        logger.info(f"Region aggregates: {df_region.count()} rows")

        df_route = aggregate_by_route(df)
        logger.info(f"Route aggregates: {df_route.count()} rows")

        df_high_risk = create_high_risk_report(df)
        logger.info(f"High-risk facilities: {df_high_risk.count()} rows")

        df_summary = create_summary_statistics(df)
        logger.info("Summary statistics created")

        df_age_group = aggregate_by_age_group(df)
        logger.info(f"Age group aggregates: {df_age_group.count()} rows")

        # Validate
        validation_passed = validate_aggregates(df_region, df_route, df_summary, validator)

        if not validation_passed:
            logger.warning("Aggregate validation failed, but proceeding with write")

        # Write aggregates
        base_output = f"{gold_path}"

        logger.info("Writing aggregates...")

        # By region
        region_path = f"{base_output}/agg_by_region/dt={partition_dt}"
        logger.info(f"  Region: {region_path}")
        df_region.write.mode("overwrite").option("compression", "snappy").parquet(region_path)

        # By route
        route_path = f"{base_output}/agg_by_route/dt={partition_dt}"
        logger.info(f"  Route: {route_path}")
        df_route.write.mode("overwrite").option("compression", "snappy").parquet(route_path)

        # High risk report
        high_risk_path = f"{base_output}/report_high_risk/dt={partition_dt}"
        logger.info(f"  High Risk: {high_risk_path}")
        df_high_risk.write.mode("overwrite").option("compression", "snappy").parquet(high_risk_path)

        # Summary statistics
        summary_path = f"{base_output}/summary_stats/dt={partition_dt}"
        logger.info(f"  Summary: {summary_path}")
        df_summary.write.mode("overwrite").option("compression", "snappy").parquet(summary_path)

        # Age group
        age_group_path = f"{base_output}/agg_by_age_group/dt={partition_dt}"
        logger.info(f"  Age Group: {age_group_path}")
        df_age_group.write.mode("overwrite").option("compression", "snappy").parquet(age_group_path)

        # Log summary statistics
        logger.info("\n" + "=" * 80)
        logger.info("SUMMARY STATISTICS")
        logger.info("=" * 80)
        summary_data = df_summary.collect()[0]
        for field in df_summary.schema.fields:
            value = summary_data[field.name]
            logger.info(f"{field.name}: {value}")
        logger.info("=" * 80)

        # Final metrics
        duration = time.time() - start_time
        metrics.log_processing_complete("Aggregate Publication", df.count(), duration)

        logger.info("=" * 80)
        logger.info("Aggregate Publication completed successfully")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"Aggregate publication failed: {str(e)}", exc_info=True)
        return 1

    finally:
        if spark:
            SparkFactory.stop_session(spark)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
