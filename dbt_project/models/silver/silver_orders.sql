-- Modelo Silver: silver_orders
-- Normalizacion y tipado de ordenes provenientes del dataset Olist E-Commerce
SELECT
    order_id,
    customer_id,
    order_status,
    purchase_timestamp,
    approved_at,
    delivered_customer_date,
    estimated_delivery_date,
    processed_at
FROM read_parquet('s3://nexus-lakehouse/silver/ecommerce/silver_orders.parquet')
WHERE order_id IS NOT NULL
