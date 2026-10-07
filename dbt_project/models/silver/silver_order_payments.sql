-- Modelo Silver: silver_order_payments
-- Normalizacion y validacion de metodos y valores de pago
SELECT
    order_id,
    TRY_CAST(payment_sequential AS INTEGER) AS payment_sequential,
    LOWER(TRIM(payment_type)) AS payment_type,
    TRY_CAST(payment_installments AS INTEGER) AS payment_installments,
    TRY_CAST(payment_value AS DOUBLE) AS payment_value,
    CURRENT_TIMESTAMP AS processed_at
FROM read_parquet('s3://nexus-lakehouse/silver/ecommerce/silver_order_payments.parquet')
WHERE payment_value > 0
