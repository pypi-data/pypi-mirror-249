from concurrent.futures import ThreadPoolExecutor
from typing import Any

from tqdm import tqdm

from s3sync.controllers.interface import SyncInterface
from s3sync.services.interface import BucketInterface
from s3sync.utils import chunks


class LocalToS3Provider(SyncInterface):
    def __init__(
        self,
        source: BucketInterface,
        target: BucketInterface,
        **kwargs,
    ):
        self.source = source
        self.target = target
        self.thread = kwargs["thread"]

    @classmethod
    def init_connection(
        cls,
        source: BucketInterface,
        target: BucketInterface,
        **kwargs,
    ):
        return cls(source, target, **kwargs)

    def sync(self, payload: tuple[int, list[dict[str, Any]]]):
        pid, data = payload
        loader = tqdm(data)
        for i, value in enumerate(loader):
            # fetch value
            resp = self.source.get_detail_file(value["Key"])
            # store file to local
            self.target.upload_file(resp["Body"], resp["Key"])
            loader.set_description(
                "Thread %s is now uploading %d file" % (pid, i), refresh=True
            )

    def sync_bucket(self):
        sources = self.source.get_list_files()
        chunk_data = chunks(sources, len(sources) // self.thread)
        with ThreadPoolExecutor(max_workers=self.thread) as p:
            p.map(self.sync, enumerate(chunk_data))
