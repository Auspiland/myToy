"""
SparkSession factory with best practices
"""
from pyspark.sql import SparkSession
from typing import Optional, Dict


class SparkFactory:
    """Factory for creating configured SparkSession instances"""

    @staticmethod
    def create_session(
            app_name: str,
            master: Optional[str] = None,
            configs: Optional[Dict[str, str]] = None
    ) -> SparkSession:
        """
        Create SparkSession with best practice configurations

        Args:
            app_name: Application name
            master: Spark master URL (None for default)
            configs: Additional Spark configurations

        Returns:
            Configured SparkSession
        """
        builder = SparkSession.builder.appName(app_name)

        # Set master if provided
        if master:
            builder = builder.master(master)

        # Default configurations
        default_configs = {
            "spark.sql.execution.arrow.pyspark.enabled": "true",
            "spark.sql.adaptive.enabled": "true",
            "spark.sql.adaptive.coalescePartitions.enabled": "true",
            "spark.sql.files.maxPartitionBytes": "134217728",  # 128MB
            "spark.sql.shuffle.partitions": "200",
            "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
            # Add more optimizations
            "spark.sql.autoBroadcastJoinThreshold": "10485760",  # 10MB
            "spark.sql.broadcastTimeout": "300",
        }

        # Apply default configs
        for key, value in default_configs.items():
            builder = builder.config(key, value)

        # Apply user configs (overrides defaults)
        if configs:
            for key, value in configs.items():
                builder = builder.config(key, value)

        # Get or create session
        spark = builder.getOrCreate()

        # Set log level to WARN to reduce noise
        spark.sparkContext.setLogLevel("WARN")

        return spark

    @staticmethod
    def stop_session(spark: SparkSession):
        """Safely stop SparkSession"""
        if spark:
            try:
                spark.stop()
            except Exception:
                pass  # Ignore errors during shutdown
