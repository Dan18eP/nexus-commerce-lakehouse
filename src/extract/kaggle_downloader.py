import os
import zipfile
from datetime import datetime
from src.utils.s3_minio import upload_file_to_s3
from src.utils.config import KAGGLE_USERNAME, KAGGLE_KEY

def download_and_upload_kaggle_dataset(dataset_identifier: str, target_bronze_folder: str = "football"):
    """
    Descarga un dataset de Kaggle y sube los archivos crudos a MinIO (Bronze).
    dataset_identifier: ej. 'davidcariboo/player-scores'
    """
    if KAGGLE_USERNAME and KAGGLE_KEY:
        os.environ['KAGGLE_USERNAME'] = KAGGLE_USERNAME
        os.environ['KAGGLE_KEY'] = KAGGLE_KEY

    import kaggle
    kaggle.api.authenticate()

    download_dir = f"/tmp/kaggle_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    os.makedirs(download_dir, exist_ok=True)

    print(f"Descargando dataset {dataset_identifier} en {download_dir}...")
    kaggle.api.dataset_download_files(dataset_identifier, path=download_dir, unzip=True)

    uploaded_files = []
    today = datetime.now().strftime("%Y-%m-%d")

    for root, _, files in os.walk(download_dir):
        for file in files:
            local_path = os.path.join(root, file)
            s3_path = f"bronze/{target_bronze_folder}/{today}/{file}"
            print(f"Subiendo {local_path} a {s3_path}...")
            upload_file_to_s3(local_path, s3_path)
            uploaded_files.append(s3_path)

    return uploaded_files

if __name__ == "__main__":
    # Test local
    print("Módulo de descarga Kaggle listo.")
