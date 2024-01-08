import argparse
import json
from enum import Enum
from typing import Tuple

from s3sync.controllers import (
    S3ToS3Provider,
    S3ToLocalProvider,
    LocalToS3Provider,
    SyncManager,
)
from s3sync.schemas import S3Config, LocalConfig
from s3sync.services import S3Services, LocalServices


class Param(Enum):
    source = "source"
    target = "target"


def get_s3_param(args: argparse.ArgumentParser.parse_args, param: Param) -> S3Config:
    match param:
        case param.source:
            if args.read_json:
                with open(args.read_json, "r") as f:
                    data = json.loads(f.read())

                return S3Config.model_validate(data["source"])

            return S3Config(
                bucket_name=args.source_bucket_name,
                region_name=args.source_region_name,
                access_key_id=args.source_access_key_id,
                secret_access_key=args.source_secret_access,
            )

        case param.target:
            if args.read_json:
                with open(args.read_json, "r") as f:
                    data = json.loads(f.read())

                return S3Config.model_validate(data["target"])

            return S3Config(
                bucket_name=args.target_bucket_name,
                region_name=args.target_region_name,
                access_key_id=args.target_access_key_id,
                secret_access_key=args.target_secret_access,
            )
        case _:
            raise ValueError("arguments is not recognize")


def get_local_param(
    args: argparse.ArgumentParser.parse_args, param: Param
) -> LocalConfig:
    match param:
        case param.source:
            if args.read_json:
                with open(args.read_json, "r") as f:
                    data = json.loads(f.read())

                return LocalConfig.model_validate(data["source"])

            return LocalConfig(path=args.source_local_path)

        case param.target:
            if args.read_json:
                with open(args.read_json, "r") as f:
                    data = json.loads(f.read())

                return LocalConfig.model_validate(data["target"])

            return LocalConfig(path=args.target_local_path)
        case _:
            raise ValueError("arguments is not recognize")


def parse_args_s3_bucket(
    args: argparse.ArgumentParser.parse_args,
) -> Tuple[S3Config, S3Config]:
    source_param = get_s3_param(args, Param.source)
    target_param = get_s3_param(args, Param.target)
    return source_param, target_param


def parse_args_s3_local(
    args: argparse.ArgumentParser.parse_args,
) -> Tuple[S3Config, LocalConfig]:
    source_param = get_s3_param(args, Param.source)
    target_param = get_local_param(args, Param.target)
    return source_param, target_param


def parse_args_local_s3(
    args: argparse.ArgumentParser.parse_args,
) -> Tuple[LocalConfig, S3Config]:
    source_param = get_local_param(args, Param.source)
    target_param = get_s3_param(args, Param.target)
    return source_param, target_param


def main():
    parser = argparse.ArgumentParser(description="s3 sync script")
    # parse data source
    parser.add_argument("-sbn", "--source-bucket-name", type=str, default="")
    parser.add_argument("-srn", "--source-region-name", type=str, default="")
    parser.add_argument("-sak", "--source-access-key-id", type=str, default="")
    parser.add_argument("-ssa", "--source-secret-access", type=str, default="")
    parser.add_argument("-slp", "--source-local-path", type=str, default="")

    # parse data target
    parser.add_argument("-tbn", "--target-bucket-name", type=str, default="")
    parser.add_argument("-trn", "--target-region-name", type=str, default="")
    parser.add_argument("-tak", "--target-access-key-id", type=str, default="")
    parser.add_argument("-tsa", "--target-secret-access", type=str, default="")
    parser.add_argument("-tlp", "--target-local-path", type=str, default="")

    # parse config
    parser.add_argument("-json", "--read-json", type=str, default="")

    # parse default syncing
    parser.add_argument("-ss3", "--sync-s3-bucket", type=bool, default=False)
    parser.add_argument("-ssl", "--sync-s3-local", type=bool, default=False)
    parser.add_argument("-sls", "--sync-local-s3", type=bool, default=False)
    parser.add_argument("-th", "--thread", type=int, default=2)

    args = parser.parse_args()

    match (args.sync_s3_bucket, args.sync_s3_local, args.sync_local_s3):
        case (True, _, _):
            source_param, target_param = parse_args_s3_bucket(args)
            provider = S3ToS3Provider.init_connection(
                source=S3Services.init_connection(source_param),
                target=S3Services.init_connection(target_param),
                thread=args.thread,
            )

        case (_, True, _):
            source_param, target_param = parse_args_s3_local(args)
            provider = S3ToLocalProvider.init_connection(
                source=S3Services.init_connection(source_param),
                target=LocalServices.init_connection(target_param),
                thread=args.thread,
            )

        case (_, _, True):
            source_param, target_param = parse_args_local_s3(args)
            provider = LocalToS3Provider.init_connection(
                source=LocalServices.init_connection(source_param),
                target=S3Services.init_connection(target_param),
                thread=args.thread,
            )

        case _:
            raise Exception("Provider not found")

    cls = SyncManager.from_provider(provider)
    cls.sync()


if __name__ == "__main__":
    main()
