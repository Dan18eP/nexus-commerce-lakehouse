# Capa Bronze: Ingestion de Datos Crudos

## 1. Proposito de la Capa
La capa Bronze (o Raw Data Layer) actua como el registro historico e inmutable de todos los datos recibidos desde fuentes externas. Su caracteristica principal es que almacena los datos tal cual fueron generados en el origen, sin alterar tipos, valores ni formatos.

## 2. Origen de Datos
* **Dataset**: Brazilian E-Commerce Public Dataset by Olist.
* **Identificador en Kaggle**: `olistbr/brazilian-ecommerce`.
* **Archivos Clave**:
  * `olist_orders_dataset.csv`: Registro de transacciones de compra, estados y timestamps de envio.
  * `olist_order_payments_dataset.csv`: Desglose financiero, metodos de pago y valores abonados.
  * `olist_order_items_dataset.csv`: Detalle por producto y vendedor.
  * `olist_customers_dataset.csv`: Informacion demografica y codigos postales.

## 3. Implementacion Tecnica
* **Modulo de Extraccion**: `src/extract/kaggle_downloader.py`.
* **Orquestador**: DAG `kaggle_bronze_ingest` (`dags/kaggle_bronze_ingest.py`).
* **Librerias Utilizadas**:
  * `kaggle`: Autenticacion segura via variables de entorno (`KAGGLE_USERNAME`, `KAGGLE_KEY`).
  * `minio`: Cliente SDK de Python para transferencias multipart hacia el Object Storage.

## 4. Estructura de Almacenamiento en MinIO
Los objetos se almacenan siguiendo una particion temporal por fecha de ejecucion:
```text
s3://nexus-lakehouse/bronze/ecommerce/{YYYY-MM-DD}/
    ├── olist_orders_dataset.csv
    ├── olist_order_payments_dataset.csv
    ├── olist_order_items_dataset.csv
    └── ...
```

## 5. Politicas de Gestion
* **Inmutabilidad**: Los archivos en Bronze no se sobreescriben; se generan nuevas particiones por fecha.
* **Trazabilidad**: Permite reproducir reprocesamientos completos si cambian las definiciones de negocio en las capas superiores.
