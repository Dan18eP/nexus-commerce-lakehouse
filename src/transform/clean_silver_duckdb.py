import duckdb
import os
from src.utils.config import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    S3_BUCKET
)

def get_duckdb_s3_connection():
    con = duckdb.connect(database=':memory:')
    con.execute("INSTALL httpfs; LOAD httpfs;")
    
    clean_endpoint = MINIO_ENDPOINT.replace("http://", "").replace("https://", "")
    
    con.execute(f"""
        SET s3_region='us-east-1';
        SET s3_access_key_id='{MINIO_ACCESS_KEY}';
        SET s3_secret_access_key='{MINIO_SECRET_KEY}';
        SET s3_endpoint='{clean_endpoint}';
        SET s3_use_ssl=false;
        SET s3_url_style='path';
    """)
    return con

def transform_bronze_to_silver_duckdb(dataset_folder="ecommerce"):
    """
    Lee órdenes y pagos de Bronze en MinIO, realiza tipado estricto, limpieza
    y almacena tablas Silver en formato Parquet particionado.
    """
    con = get_duckdb_s3_connection()
    bronze_base = f"s3://{S3_BUCKET}/bronze/{dataset_folder}/*"
    silver_base = f"s3://{S3_BUCKET}/silver/{dataset_folder}"

    print("Limpiando e ingestando orders -> Silver...")
    con.execute(f"""
        COPY (
            SELECT 
                order_id,
                customer_id,
                LOWER(TRIM(order_status)) AS order_status,
                TRY_CAST(order_purchase_timestamp AS TIMESTAMP) AS purchase_timestamp,
                TRY_CAST(order_approved_at AS TIMESTAMP) AS approved_at,
                TRY_CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_customer_date,
                TRY_CAST(order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_date,
                CURRENT_TIMESTAMP AS processed_at
            FROM read_csv_auto('{bronze_base}/*orders*.csv', header=True)
            WHERE order_id IS NOT NULL
        ) TO '{silver_base}/silver_orders.parquet' (FORMAT PARQUET);
    """)

    print("Limpiando e ingestando order_items & payments -> Silver...")
    con.execute(f"""
        COPY (
            SELECT 
                order_id,
                TRY_CAST(payment_sequential AS INTEGER) AS payment_sequential,
                LOWER(TRIM(payment_type)) AS payment_type,
                TRY_CAST(payment_installments AS INTEGER) AS payment_installments,
                TRY_CAST(payment_value AS DOUBLE) AS payment_value,
                CURRENT_TIMESTAMP AS processed_at
            FROM read_csv_auto('{bronze_base}/*order_payments*.csv', header=True)
            WHERE payment_value > 0
        ) TO '{silver_base}/silver_order_payments.parquet' (FORMAT PARQUET);
    """)

    print(f"Capa Silver generada exitosamente en {silver_base}")

if __name__ == "__main__":
    transform_bronze_to_silver_duckdb()
