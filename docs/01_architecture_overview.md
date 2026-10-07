# Arquitectura General y Diseno del Sistema

## 1. Vision General
Nexus Commerce Lakehouse es una plataforma de analitica de datos disenhada bajo el paradigma de arquitectura medallon (Bronze, Silver y Gold). Su proposito es transformar datos crudos de comercio electronico provenientes de fuentes externas en Data Marts analiticos de alto rendimiento optimizados para la toma de decisiones empresariales y el consumo en herramientas de Business Intelligence como Power BI Desktop.

## 2. Diagrama de Flujo y Topologia de Componentes

```text
+--------------------------------------------------------------------------+
|                            ORIGEN DE DATOS                               |
|               Kaggle Public API / Brazilian E-Commerce                   |
+--------------------------------------------------------------------------+
                                     |
                                     | [kaggle_bronze_ingest DAG]
                                     v
+--------------------------------------------------------------------------+
|                             CAPA BRONZE                                  |
|          MinIO Object Storage (S3-Compatible): s3://nexus-lakehouse/     |
|          Ruta: bronze/ecommerce/{YYYY-MM-DD}/*.csv                       |
|          - Almacenamiento inmutable en formato de origen                 |
|          - Sin transformaciones ni limpieza estructural                  |
+--------------------------------------------------------------------------+
                                     |
                                     | [bronze_to_silver_duckdb DAG]
                                     | Motor OLAP: DuckDB (Extension httpfs)
                                     v
+--------------------------------------------------------------------------+
|                             CAPA SILVER                                  |
|          MinIO Object Storage (S3-Compatible): s3://nexus-lakehouse/     |
|          Rutas:                                                          |
|          - silver/ecommerce/silver_orders.parquet                        |
|          - silver/ecommerce/silver_order_payments.parquet                |
|          - Esquema unificado y tipado estricto (Timestamps, Doubles)     |
|          - Filtrado de anomalias y registros invalidos                   |
|          - Almacenamiento columnar eficiente                             |
+--------------------------------------------------------------------------+
                                     |
                                     | [dbt_silver_gold DAG]
                                     | Modelado y Calidad: dbt Core + DuckDB
                                     v
+--------------------------------------------------------------------------+
|                              CAPA GOLD                                   |
|          MinIO Object Storage (S3-Compatible): s3://nexus-lakehouse/     |
|          Rutas:                                                          |
|          - gold/ecommerce/gold_daily_sales.parquet                       |
|          - gold/ecommerce/gold_payment_insights.parquet                  |
|          - Data Marts agregados para indicadores de negocio (GMV, AOV)   |
|          - Pruebas automatizadas de consistencia (not_null, unique)      |
+--------------------------------------------------------------------------+
                                     |
                                     | Conector Nativo DuckDB / ODBC / MCP
                                     v
+--------------------------------------------------------------------------+
|                        CONSUMO Y MODELADO BI                             |
|          Power BI Desktop & Microsoft Power BI Modeling MCP              |
|          - Vistas SQL analiticas sobre DuckDB                            |
|          - Modelado tabular y medidas DAX                                |
+--------------------------------------------------------------------------+
```

## 3. Justificacion de la Seleccion Tecnologica

1. **MinIO (Object Storage S3-Compatible)**:
   * Permite desacoplar el almacenamiento del procesamiento computacional.
   * Proporciona paridad completa con la API de Amazon S3, permitiendo portabilidad directa a entornos de nube publica (AWS, GCP o Azure) sin modificar el codigo de las aplicaciones.

2. **DuckDB (Motor Vectorial Columnar)**:
   * Evita la sobrecarga de infraestructura de clusters distribuidos pesados (como Spark o Trino) para datasets de tamanhos medianos y grandes (cientos de miles a decenas de millones de filas).
   * Su extension `httpfs` permite leer y escribir directamente sobre MinIO mediante streaming de rangos HTTP de archivos Parquet, consumiendo minima memoria RAM y CPU.

3. **dbt Core (Data Build Tool)**:
   * Establece un estandar de ingenieria de software (DataOps) dentro de la capa analitica: control de versiones, linaje de dependencias (DAGs de modelos) y pruebas automatizadas de integridad (`not_null`, `unique`).

4. **Apache Airflow**:
   * Orquestador estandar en la industria que ofrece trazabilidad grafica de fallos, reintentos automaticos (`retries`), alertas y gestion programada basada en tiempo o eventos.

5. **Power BI Desktop + Model Context Protocol (MCP)**:
   * Power BI ofrece capacidades visuales y de modelado DAX lideres en el mercado.
   * La integracion con el servidor `@microsoft/powerbi-modeling-mcp` habilita la asistencia mediante inteligencia artificial para la creacion, validacion y documentacion de medidas y relaciones sobre el motor tabular en ejecucion.
