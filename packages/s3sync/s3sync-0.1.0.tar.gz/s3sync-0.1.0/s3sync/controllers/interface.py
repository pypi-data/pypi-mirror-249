from abc import ABC, abstractmethod

from s3sync.services.interface import BucketInterface


class SyncInterface(ABC):
    @abstractmethod
    def init_connection(
        self,
        source: BucketInterface,
        target: BucketInterface,
        **kwargs,
    ):
        raise NotImplementedError

    @abstractmethod
    def sync_bucket(self):
        raise NotImplementedError


class SyncManager:
    def __init__(self, provider: SyncInterface):
        self.provider = provider

    @classmethod
    def from_provider(cls, source: SyncInterface):
        return cls(source)

    def sync(self):
        self.provider.sync_bucket()
