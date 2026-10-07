-- Modelo Gold: gold_payment_insights
-- Distribucion de volumen transaccional y facturacion por metodo de pago
SELECT 
    payment_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(payment_value), 2) AS total_revenue,
    ROUND(AVG(payment_value), 2) AS avg_ticket,
    CURRENT_TIMESTAMP AS updated_at
FROM {{ ref('silver_order_payments') }}
GROUP BY payment_type
ORDER BY total_revenue DESC
