import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, from_json, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

def init_triage_session():
    """Initializes a local Spark Session optimized for streaming/batch log triage."""
    return SparkSession.builder \
        .appName("EnterpriseAPITriagePipeline") \
        .master("local[*]") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

def triage_api_payloads(spark: SparkSession, input_path: str, output_path: str):
    """
    Ingests and parses high-volume API webhook event streams.
    Isolates schema drift, network timeouts, and HTTP error anomalies using PySpark.
    """
    # 1. Enforce strict JSON schema mapping for incoming API telemetry logs
    api_log_schema = StructType([
        StructField("timestamp", StringType(), True),
        StructField("tenant_id", StringType(), True),
        StructField("endpoint_path", StringType(), True),
        StructField("http_status", IntegerType(), True),
        StructField("latency_ms", DoubleType(), True),
        StructField("payload_hash", StringType(), True),
        StructField("error_details", StringType(), True)
    ])

    # 2. Ingest raw log streams (Simulating an enterprise data lake or S3/HDFS landing zone)
    raw_df = spark.read.text(input_path)
    
    # 3. Parse JSON payloads and apply telemetry rules
    parsed_df = raw_df.withColumn("data", from_json(col("value"), api_log_schema)).select("data.*")

    # 4. Automate tier-2 triage routing: categorize failures for support queues
    triaged_df = parsed_df.withColumn(
        "triage_severity",
        when(col("http_status") == 429, "RATE_LIMIT_THROTTLE")
        .when((col("http_status") >= 500) | (col("latency_ms") > 5000.0), "PLATFORM_ENGINEERING_ESCALATION")
        .when(col("http_status") == 401, "SECURITY_AUTH_FAILURE")
        .otherwise("INFO_HEALTHY")
    ).withColumn("processed_at", current_timestamp())

    # 5. Partition out anomalous logs for target engineering runbooks
    triaged_df.write \
        .mode("overwrite") \
        .partitionBy("triage_severity") \
        .parquet(output_path)

if __name__ == "__main__":
    # Local execution blueprint for GitHub CI/CD verification
    spark_session = init_triage_session()
    print("[INFO] PySpark API Triage Pipeline initialized successfully.")
