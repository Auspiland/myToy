"""
Road Risk Pipeline - Airflow DAG

This DAG orchestrates the road infrastructure risk assessment pipeline:
1. Bronze: Ingest CSV data
2. Silver: Enrich with lookups and derive features
3. Gold: Compute risk scores, levels, and aggregates

Schedule: Daily
Catchup: Disabled (only process latest)
"""
from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup


# Configuration - can be overridden by Airflow Variables
def get_config():
    """Get configuration from environment or defaults"""
    base_path = os.getenv("BASE_PATH", "C:/Users/T3Q/jeonghan/DUMMY/Spark")
    return {
        "BASE_PATH": base_path,
        "BRONZE_PATH": os.getenv("BRONZE_PATH", f"{base_path}/output/bronze"),
        "SILVER_PATH": os.getenv("SILVER_PATH", f"{base_path}/output/silver"),
        "GOLD_PATH": os.getenv("GOLD_PATH", f"{base_path}/output/gold"),
        "INPUT_CSV": os.getenv("INPUT_CSV", f"{base_path}/data/roads.csv"),
        "LOOKUP_LOAD_GRADE_CSV": os.getenv("LOOKUP_LOAD_GRADE_CSV",
                                           f"{base_path}/conf/load_grade_lookup.csv"),
    }


def log_pipeline_start(**context):
    """Log pipeline start"""
    print("=" * 80)
    print("Road Risk Pipeline Starting")
    print(f"Execution Date: {context['ds']}")
    print(f"Partition: {context['ds_nodash']}")
    print("=" * 80)


def log_pipeline_end(**context):
    """Log pipeline completion"""
    print("=" * 80)
    print("Road Risk Pipeline Completed Successfully")
    print(f"Execution Date: {context['ds']}")
    print("=" * 80)


# Default arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 11, 1),
    "email": ["admin@example.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=2),
}

# Create DAG
with DAG(
        dag_id="road_risk_pipeline",
        default_args=default_args,
        description="Road infrastructure risk assessment pipeline",
        schedule="@daily",
        catchup=False,
        tags=["spark", "risk", "roads", "infrastructure"],
        max_active_runs=1,
) as dag:

    config = get_config()

    # Environment variables for all tasks
    env_vars = {
        **config,
        "PARTITION_DT": "{{ ds_nodash }}",
        "PYTHONPATH": f"{config['BASE_PATH']}/spark_jobs",
    }

    # Start logging
    start = PythonOperator(
        task_id="log_start",
        python_callable=log_pipeline_start,
        provide_context=True,
    )

    # Bronze Layer Task Group
    with TaskGroup("bronze_layer", tooltip="Bronze Layer - Raw Data Ingestion") as bronze:

        ingest_csv = SparkSubmitOperator(
            task_id="ingest_csv",
            application=f"{config['BASE_PATH']}/spark_jobs/01_ingest_csv.py",
            name="road_ingest_bronze",
            conf={
                "spark.sql.execution.arrow.pyspark.enabled": "true",
                "spark.sql.adaptive.enabled": "true",
            },
            env_vars=env_vars,
            verbose=True,
            conn_id="spark_default",
            executor_memory="2g",
            driver_memory="1g",
        )

    # Silver Layer Task Group
    with TaskGroup("silver_layer", tooltip="Silver Layer - Data Enrichment") as silver:

        enrich_lookup = SparkSubmitOperator(
            task_id="enrich_lookup",
            application=f"{config['BASE_PATH']}/spark_jobs/02_enrich_lookup.py",
            name="road_enrich_silver",
            conf={
                "spark.sql.execution.arrow.pyspark.enabled": "true",
                "spark.sql.adaptive.enabled": "true",
            },
            env_vars=env_vars,
            verbose=True,
            conn_id="spark_default",
            executor_memory="2g",
            driver_memory="1g",
        )

    # Gold Layer Task Group
    with TaskGroup("gold_layer", tooltip="Gold Layer - Risk Analytics") as gold:

        compute_scores = SparkSubmitOperator(
            task_id="compute_scores",
            application=f"{config['BASE_PATH']}/spark_jobs/03_compute_scores.py",
            name="road_scores_gold",
            conf={
                "spark.sql.execution.arrow.pyspark.enabled": "true",
                "spark.sql.adaptive.enabled": "true",
            },
            env_vars=env_vars,
            verbose=True,
            conn_id="spark_default",
            executor_memory="2g",
            driver_memory="1g",
        )

        compute_risk = SparkSubmitOperator(
            task_id="compute_risk",
            application=f"{config['BASE_PATH']}/spark_jobs/04_compute_risk.py",
            name="road_risk_gold",
            conf={
                "spark.sql.execution.arrow.pyspark.enabled": "true",
                "spark.sql.adaptive.enabled": "true",
            },
            env_vars=env_vars,
            verbose=True,
            conn_id="spark_default",
            executor_memory="2g",
            driver_memory="1g",
        )

        publish_aggregates = SparkSubmitOperator(
            task_id="publish_aggregates",
            application=f"{config['BASE_PATH']}/spark_jobs/05_publish_aggregates.py",
            name="road_publish_gold",
            conf={
                "spark.sql.execution.arrow.pyspark.enabled": "true",
                "spark.sql.adaptive.enabled": "true",
            },
            env_vars=env_vars,
            verbose=True,
            conn_id="spark_default",
            executor_memory="2g",
            driver_memory="1g",
        )

        # Gold layer dependencies
        compute_scores >> compute_risk >> publish_aggregates

    # End logging
    end = PythonOperator(
        task_id="log_end",
        python_callable=log_pipeline_end,
        provide_context=True,
    )

    # Define pipeline flow
    start >> bronze >> silver >> gold >> end
