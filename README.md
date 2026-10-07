# 🛍️ Nexus Commerce Lakehouse

> **End-to-End Modern Data Lakehouse (Medallion Architecture)**  
> Orquestado con **Apache Airflow**, almacenamiento de objetos S3 compatible en **MinIO**, motor analítico columnar con **DuckDB** + **dbt Core**, y reportería ejecutiva en **Power BI Desktop**.

---

## 📌 Dataset Seleccionado: Olist Brazilian E-Commerce
* **Fuente**: Kaggle (`olistbr/brazilian-ecommerce`)
* **Volumen**: +100,000 pedidos reales entre 2016 y 2018 con múltiples dimensiones: clientes, vendedores, pagos, productos, geolocalización y reviews.
* **Casos de Uso de Negocio**:
  * GMV (Gross Merchandise Value) y Ticket Promedio (AOV).
  * Embudo logístico y tiempos de entrega vs estimaciones.
  * Análisis de retención, distribución de medios de pago y scoring de satisfacción.

---

## 🏛️ Arquitectura Medallón

```text
Kaggle Public API (Olist Dataset)
  │
  ▼ [Airflow Task: kaggle_bronze_ingest]
Bronze Layer (MinIO: s3://nexus-lakehouse/bronze/ecommerce/...)
  │  (Datos crudos en formato original CSV)
  ▼ [Airflow Task: DuckDB Transform]
Silver Layer (MinIO: s3://nexus-lakehouse/silver/ecommerce/...)
  │  (Tipado estricto, normalización, enriquecimiento en Parquet)
  ▼ [Airflow Task: dbt Core / DuckDB Models]
Gold Layer (MinIO: s3://nexus-lakehouse/gold/ecommerce/...)
  │  (Data Marts de ventas, pagos, SLA logístico listos para consumo)
  ▼
Power BI Desktop (Vía DuckDB Connector / MCP Modeling Server)
```

---

## 📁 Estructura del Repositorio

```text
nexus-commerce-lakehouse/
├─ dags/
│  ├─ kaggle_bronze_ingest.py        # DAG de descarga Kaggle -> MinIO Bronze
│  ├─ bronze_to_silver_duckdb.py     # DAG transformación y calidad DuckDB -> Silver
│  └─ dbt_silver_gold.py             # DAG dbt runner & data tests -> Gold
├─ src/
│  ├─ extract/
│  │  └─ kaggle_downloader.py        # Conector Kaggle API a MinIO S3
│  ├─ transform/
│  │  ├─ clean_silver_duckdb.py      # Lógica de estandarización Silver (DuckDB)
│  │  └─ aggregate_gold.py           # Agregaciones de negocio Gold
│  └─ utils/
│     ├─ config.py                   # Carga de variables de entorno
│     └─ s3_minio.py                 # Cliente y utilidades MinIO S3
├─ dbt_project/
│  ├─ dbt_project.yml
│  ├─ profiles.yml
│  ├─ models/
│  │  ├─ silver/                     # Vistas y modelos limpios
│  │  └─ gold/                       # Data Marts de analítica
│  └─ tests/
├─ gold_views.sql                    # Script SQL para levantar el catálogo DuckDB local
├─ docker-compose.yml                # Airflow + Postgres + MinIO auto-hospedado
├─ .env.example
├─ requirements.txt
└─ README.md
```

---

## 🚀 Puesta en Marcha Rápida

### 1. Variables de Entorno
Copia y completa tus claves de Kaggle en `.env`:
```bash
cp .env.example .env
```

### 2. Despliegue de Contenedores
```bash
docker compose up -d
```
* **Airflow Webserver**: http://localhost:8080 (usuario: `airflow` / clave: `airflow`)
* **MinIO Console**: http://localhost:9001 (usuario: `minioadmin` / clave: `minioadmin`)

### 3. Conexión a Power BI
1. Abre DuckDB local y ejecuta el catálogo de vistas:
   ```bash
   duckdb data/nexus_warehouse.duckdb < gold_views.sql
   ```
2. En Power BI Desktop, conéctate a la base `data/nexus_warehouse.duckdb` para consumir las vistas `gold_daily_sales` y `gold_payment_insights`.
