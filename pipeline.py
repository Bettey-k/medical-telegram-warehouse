from dagster import op, job, ScheduleDefinition
import subprocess
import sys

PYTHON = sys.executable


@op
def scrape_telegram_data():
    try:
        subprocess.run([PYTHON, "src/scrape_telegram.py"], check=True)
    except Exception as e:
        print("⚠️ scrape_telegram_data skipped:", e)


@op
def load_raw_to_postgres():
    subprocess.run([PYTHON, "src/load_raw_to_postgres.py"], check=True)


@op
def run_dbt_transformations():
    subprocess.run(
        ["dbt", "run"],
        cwd="medical_warehouse",
        check=True
    )


@op
def run_yolo_enrichment():
    try:
        subprocess.run([PYTHON, "src/yolo_detect.py"], check=True)
    except Exception as e:
        print("⚠️ run_yolo_enrichment skipped:", e)


@job
def medical_telegram_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()


daily_schedule = ScheduleDefinition(
    job=medical_telegram_pipeline,
    cron_schedule="0 2 * * *"
)
