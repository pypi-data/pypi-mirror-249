# s3-sync

Sync AWS S3 storage:
* From s3 -> s3
* FROM s3 -> local storage
* FROM local storage -> s3

## Installation
```shell
  pip install s3sync
```

## S3 sync s3 to s3

### Read from parameters
```shell
    s3-sync --sync-s3-bucket true \
        # using 5 concurrent thread default is 2
        --thread 5 \
        --source-bucket-name source-bucket \
        --source-region-name ap-southeast-1 \
        --source-access-key-id source-access-key \
        --source-secret-access source-secret \
        
        --target-bucket-name target-bucket \
        --target-region-name ap-southeast-3 \
        --target-access-key-id target-access-key \
        --target-secret-access target-secret
```

### Read from json file
* Create example json file as bellow example, you can name this file whatever

```json
{
  "source": {
    "bucket_name": "source-bucket",
    "region_name": "ap-southeast-1",
    "access_key_id": "source-access-key",
    "secret_access_key": "source-secret-key"
  },
  "target": {
    "bucket_name": "target-bucket",
    "region_name": "ap-southeast-3",
    "access_key_id": "target-access-key",
    "secret_access_key": "target-secret-key"
  }
}

```

* Then execute command `s3-sync --sync-s3-bucket true -json /home/ubuntu/config.json --thread 5`

---

## S3 sync s3 to local (*Give absolute path for this*)
### Read from parameters
```shell
    s3-sync --sync-s3-local true \
        # using 5 concurrent thread default is 2
        --thread 5 \
        --source-bucket-name source-bucket \
        --source-region-name ap-southeast-1 \
        --source-access-key-id source-access-key \
        --source-secret-access source-secret-key \
        --target-local-path /home/ubuntu/sync-s3/my-folder
```

### Read from json file
* Create example json file as bellow example, you can name this file whatever

```json
{
  "source": {
    "bucket_name": "source-bucket",
    "region_name": "ap-southeast-1",
    "access_key_id": "source-access-key",
    "secret_access_key": "source-secret-key"
  },
  "target": {
    "path": "/home/ubuntu/sync-s3/my-folder"
  }
}

```

* Then execute command `s3-sync --sync-s3-local true -json /home/ubuntu/config.json --thread 5`

---

## S3 sync local to s3

### Read from parameters
```shell
    s3-sync --sync-local-s3 true \
        # using 5 concurrent thread default is 2
        --thread 5 \
        --source-local-path /home/ubuntu/sync-s3/my-folder \
        --target-bucket-name target-bucket \
        --target-region-name ap-southeast-3 \
        --target-access-key-id target-access-key \
        --target-secret-access target-secret-key
```

### Read from json file
* Create example json file as bellow example, you can name this file whatever

```json
{
  "source": {
    "path": "/home/ubuntu/sync-s3/my-folder"
  },
  "target": {
    "bucket_name": "target-bucket-name",
    "region_name": "ap-southeast-3",
    "access_key_id": "target-access-key",
    "secret_access_key": "target-secret-key"
  }
}

```

* Then execute command `s3-sync --sync-local-s3 true -json /home/ubuntu/config.json --thread 5`

---

## Help & Bugs

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-blue.svg)](https://github.com/FerdinaKusumah/s3-sync/issues)

If you are still confused or found a bug,
please [open the issue](https://github.com/FerdinaKusumah/s3-sync/issues). All bug reports are appreciated, some
features have not been tested yet due to lack of free time.

## License

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**s3-sync** released under MIT. See `LICENSE` for more details.

