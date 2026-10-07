import duckdb
from src.transform.clean_silver_duckdb import get_duckdb_s3_connection
from src.utils.config import S3_BUCKET

def aggregate_silver_to_gold(dataset_folder="ecommerce"):
    """
    Genera Data Marts en Gold:
    1. gold_daily_sales_performance: KPI de ventas, ticket promedio, tiempos de entrega.
    2. gold_payment_method_distribution: Volumen y monto por método de pago.
    """
    con = get_duckdb_s3_connection()
    silver_orders = f"s3://{S3_BUCKET}/silver/{dataset_folder}/silver_orders.parquet"
    silver_payments = f"s3://{S3_BUCKET}/silver/{dataset_folder}/silver_order_payments.parquet"
    gold_sales = f"s3://{S3_BUCKET}/gold/{dataset_folder}/gold_daily_sales_performance.parquet"
    gold_payments = f"s3://{S3_BUCKET}/gold/{dataset_folder}/gold_payment_insights.parquet"

    print("Generando modelo Gold: Daily Sales Performance...")
    con.execute(f"""
        COPY (
            WITH orders_cte AS (
                SELECT 
                    order_id,
                    CAST(purchase_timestamp AS DATE) AS order_date,
                    order_status,
                    DATE_DIFF('day', purchase_timestamp, delivered_customer_date) AS delivery_lead_days
                FROM read_parquet('{silver_orders}')
            ),
            payments_cte AS (
                SELECT 
                    order_id,
                    SUM(payment_value) AS total_order_amount
                FROM read_parquet('{silver_payments}')
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
        ) TO '{gold_sales}' (FORMAT PARQUET);
    """)

    print("Generando modelo Gold: Payment Insights...")
    con.execute(f"""
        COPY (
            SELECT 
                payment_type,
                COUNT(*) AS total_transactions,
                ROUND(SUM(payment_value), 2) AS total_revenue,
                ROUND(AVG(payment_value), 2) AS avg_ticket,
                CURRENT_TIMESTAMP AS updated_at
            FROM read_parquet('{silver_payments}')
            GROUP BY payment_type
            ORDER BY total_revenue DESC
        ) TO '{gold_payments}' (FORMAT PARQUET);
    """)

    print(f"Modelos Gold generados exitosamente en s3://{S3_BUCKET}/gold/{dataset_folder}/")

if __name__ == "__main__":
    aggregate_silver_to_gold()
