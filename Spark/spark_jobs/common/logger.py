"""
Structured logging utility
"""
import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get configured logger with structured format

    Args:
        name: Logger name (usually __name__)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Set level
    log_level = level or 'INFO'
    logger.setLevel(getattr(logging, log_level))

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


class MetricsLogger:
    """Log metrics and statistics"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_dataframe_stats(self, df, stage: str):
        """Log DataFrame statistics"""
        try:
            count = df.count()
            self.logger.info(f"[{stage}] Row count: {count:,}")

            # Log column count
            col_count = len(df.columns)
            self.logger.info(f"[{stage}] Column count: {col_count}")

        except Exception as e:
            self.logger.warning(f"[{stage}] Could not log stats: {e}")

    def log_null_stats(self, df, stage: str):
        """Log null count statistics"""
        try:
            from pyspark.sql import functions as F

            null_counts = []
            for col in df.columns:
                null_count = df.filter(F.col(col).isNull()).count()
                if null_count > 0:
                    null_counts.append((col, null_count))

            if null_counts:
                self.logger.warning(f"[{stage}] Columns with nulls:")
                for col, count in null_counts:
                    self.logger.warning(f"  - {col}: {count:,} nulls")
            else:
                self.logger.info(f"[{stage}] No null values detected")

        except Exception as e:
            self.logger.warning(f"[{stage}] Could not log null stats: {e}")

    def log_processing_complete(self, stage: str, records: int, duration: float):
        """Log processing completion"""
        records_per_sec = records / duration if duration > 0 else 0
        self.logger.info(
            f"[{stage}] Processing complete - "
            f"Records: {records:,}, "
            f"Duration: {duration:.2f}s, "
            f"Rate: {records_per_sec:.0f} rec/s"
        )
