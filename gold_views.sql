INSTALL httpfs;
LOAD httpfs;

-- Configuración para consultar MinIO local desde DuckDB local
SET s3_region='us-east-1';
SET s3_access_key_id='minioadmin';
SET s3_secret_access_key='minioadmin';
SET s3_endpoint='127.0.0.1:9000';
SET s3_use_ssl=false;
SET s3_url_style='path';

-- Vista Gold: Rendimiento diario de ventas y tiempos logísticos
CREATE OR REPLACE VIEW gold_daily_sales AS
SELECT *
FROM read_parquet('s3://nexus-lakehouse/gold/ecommerce/gold_daily_sales_performance.parquet');

-- Vista Gold: Métricas financieras por canal de pago
CREATE OR REPLACE VIEW gold_payment_insights AS
SELECT *
FROM read_parquet('s3://nexus-lakehouse/gold/ecommerce/gold_payment_insights.parquet');

-- Vista Silver: Pedidos validados
CREATE OR REPLACE VIEW silver_orders AS
SELECT *
FROM read_parquet('s3://nexus-lakehouse/silver/ecommerce/silver_orders.parquet');
