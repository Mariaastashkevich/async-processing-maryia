import boto3


class S3Client:
    def __init__(
            self,
            endpoint_url,
            aws_access_key_id,
            aws_secret_access_key,
            region_name
    ):
        self._client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )


    def client(self):
        return self._client