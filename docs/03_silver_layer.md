# Capa Silver: Limpieza, Validacion y Estandarizacion

## 1. Proposito de la Capa
La capa Silver (o Clean/Enriched Layer) es la fuente de verdad consolidada del negocio. Toma los datos crudos depositados en la capa Bronze y aplica transformaciones de limpieza estructural, tipado de datos estricto, normalizacion de texto y filtrado de inconsistencias.

## 2. Herramientas y Motor de Ejecucion
* **Motor OLAP**: DuckDB.
* **Extension**: `httpfs` (permite realizar operaciones `read_csv_auto` y `COPY ... TO ... (FORMAT PARQUET)` directamente sobre endpoints S3 sin requerir almacenamiento local intermedio).
* **Orquestador**: DAG `bronze_to_silver_duckdb` (`dags/bronze_to_silver_duckdb.py`).
* **Modulo de Transformacion**: `src/transform/clean_silver_duckdb.py`.

## 3. Transformaciones Aplicadas

### Tabla: `silver_orders`
* **Limpieza de Identificadores**: Validacion de no nulidad en `order_id` y `customer_id`.
* **Normalizacion de Cadenas**: Aplicacion de funciones `LOWER(TRIM(...))` en `order_status`.
* **Casteo Temporal Estricto**:
  * Conversion de formatos de cadena a tipos nativos `TIMESTAMP` para `purchase_timestamp`, `approved_at`, `delivered_customer_date` y `estimated_delivery_date` mediante `TRY_CAST`.
* **Metadatos de Auditoria**: Incorporacion del campo `processed_at` con timestamp del sistema.

### Tabla: `silver_order_payments`
* **Tipado Numerico**: Conversion de `payment_sequential` y `payment_installments` a enteros (`INTEGER`).
* **Conversion Monetaria**: Casteo de `payment_value` a punto flotante de precision (`DOUBLE`).
* **Filtrado de Reglas de Negocio**: Eliminacion de registros con montos menores o iguales a cero (`payment_value > 0`).

## 4. Formato de Salida y Ventajas
* **Formato**: Apache Parquet.
* **Beneficios**:
  * Compresion columnar con Snappy.
  * Reduccion de hasta un 70% en el espacio de almacenamiento respecto al CSV original.
  * Lectura selectiva de columnas (projection pushdown) y filtrado a nivel de bloques (predicate pushdown).

## 5. Destino en MinIO
```text
s3://nexus-lakehouse/silver/ecommerce/
    ├── silver_orders.parquet
    └── silver_order_payments.parquet
```
