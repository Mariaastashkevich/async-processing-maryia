from services.storage.s3_client import S3Client


class StorageService:
    def __init__(self, client: S3Client):
        self.client = client

    def upload_file(self, bucket, key, file_name):
        self.client.client().upload_file(
            Filename=file_name,
            Bucket=bucket,
            Key=key
        )
