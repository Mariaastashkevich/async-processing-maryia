import uuid
from pathlib import Path
from typing import Tuple

from services.storage.s3_client import S3Client


class StorageService:
    def __init__(self, client: S3Client, temp_dir: Path):
        self.client = client
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def upload_file(self, bucket, key, file_name):
        self.client.client().upload_file(
            Filename=str(file_name),
            Bucket=bucket,
            Key=key
        )

    def download_to_temp(self, uri: str, job_id: str) -> Path:
        """
        Скачивает файл из хранилища во временную директорию
        и возвращает локальный Path
        """
        bucket, key = self._parse_s3_uri(uri)

        job_dir = self.temp_dir / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        local_path = job_dir / Path(key).name

        self.client.client().download_file(
            Filename=local_path,
            Bucket=bucket,
            Key=key,
        )
        return local_path


    @staticmethod
    def _parse_s3_uri(uri: str) -> Tuple[str, str]:
        # s3://{bucket}/{key} -> (bucket, key)
        if not uri.startswith('s3://'):
            raise ValueError(f"Invalid S3 URI: {uri}")

        _, _, rest = uri.partition("s3://")
        bucket, _, key = rest.partition("/")

        if not bucket or not key:
            raise ValueError(f"Invalid S3 URI: {uri}")

        return bucket, key


