import io
import os.path
from typing import Any

import boto3

from s3sync.schemas import S3Config
from s3sync.services.interface import BucketInterface


class S3Services(BucketInterface):
    def __init__(self, client: boto3.client, config: S3Config):
        self.client = client
        self.config = config

    @classmethod
    def init_connection(cls, config: S3Config) -> "S3Services":
        conn = boto3.client(
            "s3",
            region_name=config.region_name,
            aws_access_key_id=config.access_key_id,
            aws_secret_access_key=config.secret_access_key,
        )
        return cls(conn, config)

    def get_list_files(self) -> list[dict[str, Any]]:
        resp = self.client.list_objects(Bucket=self.config.bucket_name)
        return resp["Contents"]

    def get_detail_file(self, file_name: str) -> dict[str, Any]:
        resp = self.client.get_object(Bucket=self.config.bucket_name, Key=file_name)
        return resp

    def upload_file(self, body: io.StringIO, file_name: str) -> None:
        self.client.upload_fileobj(body, self.config.bucket_name, file_name)
        return None

    def download_file(self, path: str, file_name: str) -> None:
        full_path = os.path.join(path, file_name)
        with open(full_path, "wb") as f:
            self.client.download_fileobj(self.config.bucket_name, file_name, f)

        return None
