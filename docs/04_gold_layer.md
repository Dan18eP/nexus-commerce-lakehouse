# Capa Gold: Modelado Analitico y Data Marts

## 1. Proposito de la Capa
La capa Gold (o Business/Curated Layer) contiene modelos dimensionales y Data Marts de agregacion listos para ser consumidos directamente por directores, analistas de negocio y paneles de control en Power BI Desktop. Las transformaciones reducen la complejidad de calculo en el reporteador.

## 2. Herramientas y Framework
* **Framework de Modelado**: dbt Core (`dbt-core` y `dbt-duckdb`).
* **Motor OLAP**: DuckDB con extension `httpfs`.
* **Orquestador**: DAG `dbt_silver_gold` (`dags/dbt_silver_gold.py`).
* **Modulo de Soporte**: `src/transform/aggregate_gold.py`.

## 3. Data Marts Generados

### Modelo 1: `gold_daily_sales`
* **Archivo SQL**: `dbt_project/models/gold/gold_daily_sales.sql`.
* **Granularidad**: Diaria (`order_date`).
* **Metricas Calculadas**:
  * `total_orders`: Conteo total de ordenes confirmadas por dia.
  * `gross_merchandise_value`: Facturacion bruta diaria agregada.
  * `average_order_value`: Ticket promedio por pedido (AOV).
  * `avg_delivery_days`: Promedio de dias transcurridos entre la compra y la recepcion por el cliente (`delivery_lead_days`).
* **Uso en Negocio**: Monitoreo de salud financiera, estacionalidad de ventas y cumplimiento de acuerdos de nivel de servicio (SLA) de despacho.

### Modelo 2: `gold_payment_insights`
* **Archivo SQL**: `dbt_project/models/gold/gold_payment_insights.sql`.
* **Granularidad**: Por tipo de pago (`payment_type`: credit_card, boleto, voucher, debit_card).
* **Metricas Calculadas**:
  * `total_transactions`: Conteo de operaciones por metodo.
  * `total_revenue`: Recaudacion total canalizada por el medio de pago.
  * `avg_ticket`: Monto medio por transaccion segun el metodo seleccionado.
* **Uso en Negocio**: Negociacion de comisiones bancarias y pasarelas de pago, evaluacion de riesgo crediticio y penetracion de pagos digitales.

## 4. Pruebas de Calidad de Datos (dbt Tests)
Configuradas en `dbt_project/tests/schema.yml`:
* `not_null`: Garantiza que campos clave como `order_date`, `payment_type` y montos agregados no contengan valores nulos.
* `unique`: Garantiza la unicidad de las claves primarias en los Data Marts diarios y por categoria de pago.

## 5. Destino en MinIO
```text
s3://nexus-lakehouse/gold/ecommerce/
    ├── gold_daily_sales.parquet
    └── gold_payment_insights.parquet
```
