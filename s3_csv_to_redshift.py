from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.amazon.aws.transfers.s3_to_s3 import S3CopyObjectOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.hooks.redshift_sql import RedshiftSQLHook
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator
import pandas as pd
import io
import boto3

# ======================
# Config
# ======================
SOURCE_BUCKET = "sanjib-dev-bucket"
SOURCE_KEY = "input/data.csv"
INTERMEDIATE_BUCKET = "my-intermediate-bucket"
INTERMEDIATE_KEY = "processed/data.parquet"
TRANSFORMED_BUCKET = "sanjib-prod-bucket"
TRANSFORMED_KEY = "final/data.parquet"
REDSHIFT_TABLE = "public.my_table"
REDSHIFT_CONN_ID = "my_redshift"
AWS_CONN_ID = "aws_default"
IAM_ROLE = "arn:aws:iam::123456789012:role/MyRedshiftRole"

# ======================
# Python Functions
# ======================

def convert_csv_to_parquet(**kwargs):
    s3 = S3Hook(aws_conn_id=AWS_CONN_ID)
    file_obj = s3.get_key(SOURCE_KEY, bucket_name=SOURCE_BUCKET)
    df = pd.read_csv(io.BytesIO(file_obj.get()['Body'].read()))

    out_buffer = io.BytesIO()
    df.to_parquet(out_buffer, index=False)

    s3.load_file_obj(
        file_obj=io.BytesIO(out_buffer.getvalue()),
        key=INTERMEDIATE_KEY,
        bucket_name=INTERMEDIATE_BUCKET,
        replace=True
    )
    print(f"✅ CSV converted to Parquet and stored at s3://{INTERMEDIATE_BUCKET}/{INTERMEDIATE_KEY}")

def copy_parquet_to_redshift(**kwargs):
    redshift = RedshiftSQLHook(redshift_conn_id=REDSHIFT_CONN_ID)
    sql = f"""
        COPY {REDSHIFT_TABLE}
        FROM 's3://{TRANSFORMED_BUCKET}/{TRANSFORMED_KEY}'
        IAM_ROLE '{IAM_ROLE}'
        FORMAT AS PARQUET;
    """
    redshift.run(sql)
    print(f"✅ Data copied into Redshift table {REDSHIFT_TABLE}")

# ======================
# DAG Definition
# ======================
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="s3_csv_to_redshift_dag",
    default_args=default_args,
    description="ETL DAG: S3 CSV -> Parquet -> Spark SQL Transform -> Redshift",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # Step 1: Convert CSV to Parquet
    csv_to_parquet = PythonOperator(
        task_id="csv_to_parquet",
        python_callable=convert_csv_to_parquet,
    )

    # Step 2: Run Spark SQL Transformations
    spark_transform = SparkSubmitOperator(
        task_id="spark_transform",
        application="/opt/airflow/dags/spark_jobs/transform_parquet.py",  # Spark job file path
        conn_id="spark_default",
        application_args=[
            f"s3://{INTERMEDIATE_BUCKET}/{INTERMEDIATE_KEY}",
            f"s3://{TRANSFORMED_BUCKET}/{TRANSFORMED_KEY}"
        ],
        verbose=True
    )

    # Step 3: Copy final data into Redshift
    load_redshift = PythonOperator(
        task_id="load_redshift",
        python_callable=copy_parquet_to_redshift,
    )

    # Workflow order
    csv_to_parquet >> spark_transform >> load_redshift
