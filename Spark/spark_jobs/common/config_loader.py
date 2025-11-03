"""
Configuration loader with environment variable override support
"""
import os
import yaml
from typing import Dict, Any


class ConfigLoader:
    """Load configuration from YAML with environment variable overrides"""

    def __init__(self, config_path: str = None):
        """
        Initialize config loader

        Args:
            config_path: Path to YAML config file (optional)
        """
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value with environment variable override

        Priority:
        1. Environment variable (uppercase, with prefix)
        2. Config file value
        3. Default value

        Args:
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value
        """
        # Try environment variable first (e.g., RISK_BASE_PATH)
        env_key = f"RISK_{key.upper()}"
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return env_value

        # Try direct environment variable
        env_value = os.environ.get(key)
        if env_value is not None:
            return env_value

        # Try config file
        if key in self.config:
            return self.config[key]

        # Return default
        return default

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        result = self.config.copy()

        # Override with environment variables
        for key in result.keys():
            env_key = f"RISK_{key.upper()}"
            if env_key in os.environ:
                result[key] = os.environ[env_key]

        return result

    @classmethod
    def from_env(cls) -> 'ConfigLoader':
        """Create ConfigLoader from environment variables only"""
        loader = cls()

        # Default configuration
        base_path = os.environ.get("BASE_PATH", "/opt/road")
        loader.config = {
            "base_path": base_path,
            "bronze_path": os.environ.get("BRONZE_PATH", f"{base_path}/output/bronze"),
            "silver_path": os.environ.get("SILVER_PATH", f"{base_path}/output/silver"),
            "gold_path": os.environ.get("GOLD_PATH", f"{base_path}/output/gold"),
            "input_csv": os.environ.get("INPUT_CSV", f"{base_path}/data/roads.csv"),
            "lookup_load_grade_csv": os.environ.get("LOOKUP_LOAD_GRADE_CSV",
                                                     f"{base_path}/conf/load_grade_lookup.csv"),
            "partition_dt": os.environ.get("PARTITION_DT", "20251103"),
        }

        return loader
