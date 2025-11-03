"""
Data quality validation framework
"""
from pyspark.sql import DataFrame, functions as F
from typing import List, Dict, Any, Optional
import logging


class DataQualityValidator:
    """Validate data quality with configurable rules"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.validation_results = []

    def reset(self):
        """Reset validation results"""
        self.validation_results = []

    def validate_not_empty(self, df: DataFrame, name: str = "DataFrame") -> bool:
        """Validate DataFrame is not empty"""
        count = df.count()
        passed = count > 0

        result = {
            "rule": "not_empty",
            "name": name,
            "passed": passed,
            "count": count
        }
        self.validation_results.append(result)

        if passed:
            self.logger.info(f"✓ {name} is not empty ({count:,} rows)")
        else:
            self.logger.error(f"✗ {name} is empty!")

        return passed

    def validate_schema(self, df: DataFrame, required_columns: List[str], name: str = "DataFrame") -> bool:
        """Validate required columns exist"""
        df_columns = set(df.columns)
        required_set = set(required_columns)
        missing = required_set - df_columns

        passed = len(missing) == 0

        result = {
            "rule": "schema_check",
            "name": name,
            "passed": passed,
            "missing_columns": list(missing)
        }
        self.validation_results.append(result)

        if passed:
            self.logger.info(f"✓ {name} has all required columns")
        else:
            self.logger.error(f"✗ {name} missing columns: {missing}")

        return passed

    def validate_null_threshold(
            self,
            df: DataFrame,
            columns: List[str],
            max_null_ratio: float = 0.9,
            name: str = "DataFrame"
    ) -> bool:
        """Validate null ratio is below threshold"""
        total_rows = df.count()
        all_passed = True

        for col in columns:
            null_count = df.filter(F.col(col).isNull()).count()
            null_ratio = null_count / total_rows if total_rows > 0 else 0

            passed = null_ratio <= max_null_ratio

            result = {
                "rule": "null_threshold",
                "name": f"{name}.{col}",
                "passed": passed,
                "null_count": null_count,
                "null_ratio": null_ratio,
                "threshold": max_null_ratio
            }
            self.validation_results.append(result)

            if passed:
                self.logger.info(
                    f"✓ {name}.{col} null ratio: {null_ratio:.2%} (threshold: {max_null_ratio:.2%})")
            else:
                self.logger.error(
                    f"✗ {name}.{col} null ratio: {null_ratio:.2%} exceeds threshold {max_null_ratio:.2%}")
                all_passed = False

        return all_passed

    def validate_range(
            self,
            df: DataFrame,
            column: str,
            min_val: Optional[float] = None,
            max_val: Optional[float] = None,
            name: str = "DataFrame"
    ) -> bool:
        """Validate numeric column is within range"""
        stats = df.agg(
            F.min(column).alias("min_val"),
            F.max(column).alias("max_val")
        ).collect()[0]

        actual_min = stats["min_val"]
        actual_max = stats["max_val"]

        passed = True
        if min_val is not None and actual_min is not None and actual_min < min_val:
            passed = False
        if max_val is not None and actual_max is not None and actual_max > max_val:
            passed = False

        result = {
            "rule": "range_check",
            "name": f"{name}.{column}",
            "passed": passed,
            "actual_min": actual_min,
            "actual_max": actual_max,
            "expected_min": min_val,
            "expected_max": max_val
        }
        self.validation_results.append(result)

        if passed:
            self.logger.info(
                f"✓ {name}.{column} range: [{actual_min}, {actual_max}] within bounds")
        else:
            self.logger.error(
                f"✗ {name}.{column} range: [{actual_min}, {actual_max}] outside bounds [{min_val}, {max_val}]")

        return passed

    def validate_uniqueness(
            self,
            df: DataFrame,
            columns: List[str],
            name: str = "DataFrame"
    ) -> bool:
        """Validate column combination is unique"""
        total_rows = df.count()
        distinct_rows = df.select(columns).distinct().count()

        passed = total_rows == distinct_rows

        result = {
            "rule": "uniqueness",
            "name": f"{name}.{'+'.join(columns)}",
            "passed": passed,
            "total_rows": total_rows,
            "distinct_rows": distinct_rows,
            "duplicates": total_rows - distinct_rows
        }
        self.validation_results.append(result)

        if passed:
            self.logger.info(f"✓ {name} columns {columns} are unique")
        else:
            duplicates = total_rows - distinct_rows
            self.logger.warning(f"⚠ {name} has {duplicates:,} duplicate rows on {columns}")

        return passed

    def get_results(self) -> List[Dict[str, Any]]:
        """Get all validation results"""
        return self.validation_results

    def all_passed(self) -> bool:
        """Check if all validations passed"""
        return all(r["passed"] for r in self.validation_results)

    def summary(self) -> str:
        """Get validation summary"""
        total = len(self.validation_results)
        passed = sum(1 for r in self.validation_results if r["passed"])
        failed = total - passed

        return f"Validation Summary: {passed}/{total} passed, {failed} failed"
