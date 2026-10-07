-- Modelo Silver: silver_orders
-- Normalizacion y tipado de ordenes provenientes del dataset Olist E-Commerce
SELECT
    order_id,
    customer_id,
    LOWER(TRIM(order_status)) AS order_status,
    TRY_CAST(order_purchase_timestamp AS TIMESTAMP) AS purchase_timestamp,
    TRY_CAST(order_approved_at AS TIMESTAMP) AS approved_at,
    TRY_CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_customer_date,
    TRY_CAST(order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_date,
    CURRENT_TIMESTAMP AS processed_at
FROM read_parquet('s3://nexus-lakehouse/silver/ecommerce/silver_orders.parquet')
WHERE order_id IS NOT NULL
