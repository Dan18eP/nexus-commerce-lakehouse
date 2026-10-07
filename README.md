# Nexus Commerce Lakehouse

Pipeline de datos end-to-end con arquitectura medallon (Bronze, Silver y Gold) para la ingestion, procesamiento analitico y modelado de datos de comercio electronico a gran escala.

El stack esta construido con tecnologias de codigo abierto y componentes auto-hospedados utilizando Docker, MinIO como almacenamiento de objetos compatible con S3, DuckDB como motor de procesamiento columnar en memoria, dbt Core para modelado y pruebas de calidad, Apache Airflow para la orquestacion del flujo y Power BI Desktop para el consumo analitico.

---

## 1. Dataset y Dominio del Negocio

* **Dataset de Referencia**: Brazilian E-Commerce Public Dataset by Olist (`olistbr/brazilian-ecommerce`) en Kaggle.
* **Volumen**: Mas de 100,000 pedidos con registros detallados entre 2016 y 2018.
* **Alcance Analitico**:
  * Metricas de conversion, Gross Merchandise Value (GMV) y valor de ticket promedio (AOV).
  * Monitoreo del ciclo logistico: fecha de compra, aprobacion, despacho, entrega efectiva y desviaciones frente a la fecha estimada.
  * Distribucion transaccional por metodos de pago y plazos de financiamiento.

---

## 2. Arquitectura Medallon

```text
+-------------------------------------------------------------+
|               Kaggle Public API / CLI                       |
+-------------------------------------------------------------+
                              |
                              v [DAG: kaggle_bronze_ingest]
+-------------------------------------------------------------+
|                        CAPA BRONZE                          |
| MinIO S3: s3://nexus-lakehouse/bronze/ecommerce/{fecha}/    |
| - Archivos crudos en formato original (CSV / Comprimidos)   |
| - Sin alteraciones, historico inmutable de ingesta          |
+-------------------------------------------------------------+
                              |
                              v [DAG: bronze_to_silver_duckdb]
+-------------------------------------------------------------+
|                        CAPA SILVER                          |
| MinIO S3: s3://nexus-lakehouse/silver/ecommerce/            |
| - Limpieza estructural, tipado de fechas y valores          |
| - Filtro de registros inconsistentes                        |
| - Formato columnar optimizado: Parquet                      |
+-------------------------------------------------------------+
                              |
                              v [DAG: dbt_silver_gold]
+-------------------------------------------------------------+
|                         CAPA GOLD                           |
| MinIO S3: s3://nexus-lakehouse/gold/ecommerce/              |
| - Modelos agregados y Data Marts con dbt Core y DuckDB      |
| - gold_daily_sales: metricas diarias de pedidos y logistica |
| - gold_payment_insights: facturacion por canal de pago      |
+-------------------------------------------------------------+
                              |
                              v [Conector DuckDB / DirectQuery / ODBC]
+-------------------------------------------------------------+
|                      POWER BI DESKTOP                       |
| - Consumo de vistas SQL definidas sobre archivos Parquet    |
| - Soporte de integracion via Power BI Authoring MCP Server  |
+-------------------------------------------------------------+
```

---

## 3. Componentes Tecnologicos

| Funcion | Tecnologia | Detalle |
|---|---|---|
| Orquestacion | Apache Airflow 2.8.1 | Programacion, reintentos y linaje de tareas en Python. |
| Object Storage | MinIO | Almacenamiento local compatible con la API de Amazon S3. |
| Metastore / Catalogo | PostgreSQL 13 | Almacenamiento de metadatos de Apache Airflow. |
| Motor OLAP | DuckDB | Motor columnar integrado de alta velocidad para transformaciones S3. |
| Modelado y Calidad | dbt Core + dbt-duckdb | Transformaciones declarativas SQL, linaje y pruebas unitarias de esquema. |
| Extraccion | Kaggle API CLI | Descarga programada de datasets publicos. |
| Visualizacion y BI | Power BI Desktop | Modelado semantico, DAX y reportes ejecutivos. |
| Integracion AI / Modelado | Model Context Protocol (MCP) | Integracion con `@microsoft/powerbi-modeling-mcp`. |

---

## 4. Estructura del Repositorio

```text
nexus-commerce-lakehouse/
├── dags/
│   ├── kaggle_bronze_ingest.py        # DAG de descarga y carga a MinIO Bronze
│   ├── bronze_to_silver_duckdb.py     # DAG de transformacion y calidad a Silver
│   └── dbt_silver_gold.py             # DAG de ejecucion de modelos y pruebas dbt
├── dbt_project/
│   ├── dbt_project.yml                # Configuracion general del proyecto dbt
│   ├── profiles.yml                   # Perfil de conexion dbt con DuckDB y credenciales S3
│   ├── models/
│   │   ├── silver/                    # Modelos SQL para normalizacion (silver_orders, etc.)
│   │   └── gold/                      # Data Marts de analitica (gold_daily_sales, etc.)
│   └── tests/
│       └── schema.yml                 # Reglas de validacion (not_null, unique, etc.)
├── src/
│   ├── extract/
│   │   └── kaggle_downloader.py       # Descargador autenticado de Kaggle
│   ├── transform/
│   │   ├── clean_silver_duckdb.py     # Script DuckDB de ingestion a Silver
│   │   └── aggregate_gold.py          # Script DuckDB de agregacion a Gold
│   └── utils/
│       ├── config.py                  # Gestion centralizada de variables de entorno
│       └── s3_minio.py                # Wrapper para operaciones en MinIO S3
├── docs/                              # Documentacion tecnica detallada
│   ├── 01_architecture_overview.md    # Topologia, justificacion y flujo global
│   ├── 02_bronze_layer.md             # Ingestion de datos crudos (Kaggle API)
│   ├── 03_silver_layer.md             # Limpieza, casteo y conversion a Parquet
│   ├── 04_gold_layer.md               # Modelado con dbt Core y Data Marts
│   ├── 05_powerbi_and_mcp_integration.md # Consumo en Power BI y asistente IA MCP
│   └── 06_operations_and_deployment.md# Guia de operacion de contenedores Docker
├── docker-compose.yml                 # Definicion de servicios: Airflow, Postgres y MinIO
├── gold_views.sql                     # Script SQL para generacion de vistas en DuckDB
├── requirements.txt                   # Librerias de Python requeridas
├── .env.example                       # Plantilla de variables de entorno
├── .gitignore                         # Exclusiones de Git (secretos, data, logs)
└── README.md                          # Documentacion tecnica del sistema
```

---

## 5. Requisitos Previos

* Docker Desktop o Docker Engine con Docker Compose v2.
* Python 3.10 o superior (para ejecucion de scripts locales o dbt fuera de contenedor).
* Cuenta de Kaggle con API Token generado (`KAGGLE_USERNAME` y `KAGGLE_KEY`).
* Power BI Desktop instalado en entorno Windows.

---

## 6. Guia de Instalacion y Configuracion

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/Dan18eP/nexus-commerce-lakehouse.git
cd nexus-commerce-lakehouse
```

### Paso 2: Configurar variables de entorno
Copiar el archivo de plantilla a `.env`:
```bash
cp .env.example .env
```

Completar los siguientes valores clave:
```env
KAGGLE_DATASET=olistbr/brazilian-ecommerce
KAGGLE_USERNAME=tu_usuario_kaggle
KAGGLE_KEY=tu_api_key_kaggle

MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_ENDPOINT=minio:9000
MINIO_EXTERNAL_ENDPOINT=localhost:9000
S3_BUCKET=nexus-lakehouse
```

### Paso 3: Inicializar la infraestructura con Docker Compose
Ejecutar el levantamiento de los contenedores:
```bash
docker compose up -d
```

Validar el acceso a los servicios:
* **Airflow UI**: http://localhost:8080 (credenciales por defecto: `airflow` / `airflow`)
* **MinIO Console**: http://localhost:9001 (credenciales por defecto: `minioadmin` / `minioadmin`)

---

## 7. Ejecucion de los Pipelines en Airflow

1. **`kaggle_bronze_ingest`**:
   * Descarga los archivos crudos mediante la API de Kaggle.
   * Organiza la estructura temporal `bronze/ecommerce/{yyyy-mm-dd}/` en el bucket `nexus-lakehouse`.

2. **`bronze_to_silver_duckdb`**:
   * Lee directamente los CSV desde MinIO mediante la extension `httpfs` de DuckDB.
   * Aplica saneamiento, casteo de columnas de fecha, limpieza de texto y filtros de validacion.
   * Escribe archivos Parquet comprimidos en `silver/ecommerce/`.

3. **`dbt_silver_gold`**:
   * Ejecuta `dbt run` para procesar los modelos de negocio.
   * Genera las tablas agregadas en `gold/ecommerce/`.
   * Ejecuta `dbt test` para certificar la integridad referencial y nulidad de los datos.

---

## 8. Integracion con Power BI Desktop

### Opcion A: Consulta directa mediante catalogo DuckDB
1. Abrir DuckDB en la consola local o mediante script para crear el catalogo:
   ```bash
   duckdb data/nexus_warehouse.duckdb < gold_views.sql
   ```
2. En Power BI Desktop, seleccionar **Obtener datos** -> **Mas...** -> **DuckDB**.
3. Indicar la ruta del archivo `data/nexus_warehouse.duckdb`.
4. Importar las vistas analiticas `gold_daily_sales` y `gold_payment_insights`.

### Opcion B: Interaccion con Model Context Protocol (MCP)
El proyecto incluye compatibilidad con el servidor de modelado `@microsoft/powerbi-modeling-mcp`. Esto permite a asistentes de inteligencia artificial conectarse con la instancia activa de Power BI Desktop (`PBIDesktop.exe` / `msmdsrv`) para:
* Inspeccionar esquemas de tablas y metadatos del modelo tabular.
* Generar y validar medidas en lenguaje DAX.
* Documentar relaciones y jerarquias del modelo.

---

## 9. Licencia

Este proyecto esta licenciado bajo la Licencia MIT.
