from dagster import op, job, ScheduleDefinition
import subprocess
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


@op
def load_raw_to_postgres():
    subprocess.run(
        [sys.executable, "src/load_raw_to_postgres.py"],
        cwd=PROJECT_ROOT,
        check=True
    )


@op
def run_dbt_transformations():
    subprocess.run(
        ["dbt", "run"],
        cwd=os.path.join(PROJECT_ROOT, "medical_warehouse"),
        check=True
    )


@op
def run_yolo_enrichment():
    subprocess.run(
        [sys.executable, "src/yolo_detect.py"],
        cwd=PROJECT_ROOT,
        check=True
    )


@job
def medical_telegram_pipeline():
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()


daily_schedule = ScheduleDefinition(
    job=medical_telegram_pipeline,
    cron_schedule="0 2 * * *"
)
