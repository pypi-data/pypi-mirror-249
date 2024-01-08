import io
from abc import ABC, abstractmethod
from typing import Any


class BucketInterface(ABC):
    @abstractmethod
    def get_list_files(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_detail_file(self, file_name: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def upload_file(self, body: io.StringIO, file_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def download_file(self, path: str, file_name: str) -> None:
        raise NotImplementedError
