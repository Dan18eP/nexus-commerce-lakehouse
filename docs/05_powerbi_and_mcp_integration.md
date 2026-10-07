# Consumo en Power BI Desktop e Integracion con IA (MCP)

## 1. Estrategia de Consumo Analitico
Para maximizar el desempenho en Power BI Desktop, las consultas analiticas no se ejecutan directamente sobre archivos CSV crudos, sino sobre las vistas y tablas Parquet de la capa Gold optimizadas por DuckDB.

## 2. Metodos de Conexion

### Opcion 1: Catalogo DuckDB y Conector Nativo / ODBC (Recomendada)
1. DuckDB expone un catalogo unificado de vistas SQL configurado en `gold_views.sql`:
   ```sql
   INSTALL httpfs;
   LOAD httpfs;

   SET s3_region='us-east-1';
   SET s3_access_key_id='minioadmin';
   SET s3_secret_access_key='minioadmin';
   SET s3_endpoint='127.0.0.1:9000';
   SET s3_use_ssl=false;
   SET s3_url_style='path';

   CREATE OR REPLACE VIEW gold_daily_sales AS
   SELECT * FROM read_parquet('s3://nexus-lakehouse/gold/ecommerce/gold_daily_sales.parquet');

   CREATE OR REPLACE VIEW gold_payment_insights AS
   SELECT * FROM read_parquet('s3://nexus-lakehouse/gold/ecommerce/gold_payment_insights.parquet');
   ```

2. Ejecutar la compilacion del catalogo local:
   ```bash
   duckdb data/nexus_warehouse.duckdb < gold_views.sql
   ```

3. Desde **Power BI Desktop**:
   * Seleccionar **Obtener datos** -> **DuckDB**.
   * Indicar la ruta del archivo `data/nexus_warehouse.duckdb`.
   * Cargar las tablas `gold_daily_sales` y `gold_payment_insights`.

---

## 3. Integracion de Automatizacion con IA: Model Context Protocol (MCP)

### Proposito de la Integracion
En el marco de la automatizacion con IA, se configuro el servidor oficial de Microsoft para Power BI:
`@microsoft/powerbi-modeling-mcp`.

### Que permite esta integracion
1. **Conexion directa con la instancia local de Power BI Desktop**:
   * Se conecta al motor tabular embebido de Analysis Services (`msmdsrv.exe`, puerto local activo).
2. **Capacidades asistidas por Agente de IA**:
   * **Inspeccion Semantica**: El agente puede consultar el esquema de tablas, relaciones y tipos de datos del modelo en vivo.
   * **Generacion y Validacion de Medidas DAX**: Creacion de formulas de acumulados anuales (YTD), crecimientos intermensuales (MoM) y calculos de percentiles de entrega.
   * **Documentacion del Modelo**: Descripcion automatica de medidas y columnas para el diccionario corporativo.

### Configuracion de MCP en el Entorno
El servidor se encuentra registrado en el archivo de configuracion global de MCP (`~/.gemini/config/mcp_config.json`):
```json
{
  "mcpServers": {
    "powerbi": {
      "command": "npx",
      "args": [
        "-y",
        "@microsoft/powerbi-modeling-mcp"
      ],
      "env": {}
    }
  }
}
```
Esto habilita la creacion asistida y versionamiento de artefactos analiticos mediante IA sin abandonar el entorno de desarrollo.
