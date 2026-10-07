{{ config(
    materialized='external',
    location='s3://nexus-lakehouse/gold/ecommerce/gold_daily_sales.parquet'
) }}

-- Modelo Gold: gold_daily_sales
-- Agregacion ejecutiva de ventas diarias, ticket promedio y rendimiento logistico
WITH orders_cte AS (
    SELECT 
        order_id,
        CAST(purchase_timestamp AS DATE) AS order_date,
        order_status,
        DATE_DIFF('day', purchase_timestamp, delivered_customer_date) AS delivery_lead_days
    FROM {{ ref('silver_orders') }}
),
payments_cte AS (
    SELECT 
        order_id,
        SUM(payment_value) AS total_order_amount
    FROM {{ ref('silver_order_payments') }}
    GROUP BY order_id
)
SELECT 
    o.order_date,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(p.total_order_amount), 2) AS gross_merchandise_value,
    ROUND(AVG(p.total_order_amount), 2) AS average_order_value,
    ROUND(AVG(o.delivery_lead_days), 1) AS avg_delivery_days,
    CURRENT_TIMESTAMP AS updated_at
FROM orders_cte o
INNER JOIN payments_cte p ON o.order_id = p.order_id
WHERE o.order_date IS NOT NULL
GROUP BY o.order_date
ORDER BY o.order_date DESC
