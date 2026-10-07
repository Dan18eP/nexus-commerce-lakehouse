# Guia de Operacion y Despliegue con Docker

## 1. Topologia de Contenedores

| Servicio | Imagen Base | Puertos Expuestos | Funcion |
|---|---|---|---|
| `postgres` | `postgres:13` | `5432:5432` (interno) | Metastore relacional para Apache Airflow. |
| `minio` | `cgr.dev/chainguard/minio:latest` | `9000:9000`, `9001:9001` | Almacenamiento S3 y consola web de administracion. |
| `airflow-init` | `apache/airflow:2.8.1-python3.10` | N/A (One-off) | Migracion de base de datos y creacion de usuario admin. |
| `airflow-webserver` | `apache/airflow:2.8.1-python3.10` | `8080:8080` | Interfaz grafica de usuario para administracion de DAGs. |
| `airflow-scheduler` | `apache/airflow:2.8.1-python3.10` | N/A | Monitoreo, ejecucion y programacion de tareas. |

## 2. Comandos Operativos

### Iniciar todos los servicios
```bash
docker compose up -d
```

### Verificar estado de salud de contenedores
```bash
docker ps
```

### Consultar logs del Webserver o Scheduler
```bash
docker logs datapipeline-airflow-webserver-1 --tail 50 -f
docker logs datapipeline-airflow-scheduler-1 --tail 50 -f
```

### Detener los servicios sin eliminar volumenes
```bash
docker compose stop
```

### Reiniciar el entorno completo
```bash
docker compose down
docker compose up -d
```

## 3. Credenciales y Puntos de Acceso

* **Apache Airflow**:
  * URL: `http://localhost:8080`
  * Usuario: `airflow`
  * Contrasenha: `airflow`

* **MinIO Console**:
  * URL: `http://localhost:9001`
  * Endpoint API S3: `http://localhost:9000`
  * Usuario: `minioadmin`
  * Contrasenha: `minioadmin`
  * Bucket Primario: `nexus-lakehouse`
