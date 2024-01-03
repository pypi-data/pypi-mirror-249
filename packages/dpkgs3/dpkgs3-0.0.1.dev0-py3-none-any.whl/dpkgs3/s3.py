import os
import hashlib
from typing import Any, Dict, Union

import boto3
import botocore


class S3:
    def __init__(
        self,
        bucket: str,
        access_policy: str = "public-read",
        prefix: Union[str, None] = None,
        encryption: bool = False,
    ):
        self.client = boto3.client("s3")
        self.bucket = bucket
        self.access_policy = access_policy
        self.prefix = prefix
        self.encryption = encryption

    def full_path(self, subpath: str):
        return os.path.join(self.prefix or "", subpath)

    def exists(self, path: str):
        try:
            return self.client.head_object(Bucket=self.bucket, Key=self.full_path(path))
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return None
            else:
                raise

    def read(self, path: str):
        try:
            response = self.client.get_object(
                Bucket=self.bucket, Key=self.full_path(path)
            )
            return response["Body"].read()
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:
                raise

    def store(
        self,
        path: str,
        filename: Union[str, None] = None,
        content_type: str = "application/x-debian-package",
        cache_control: Union[str, None] = None,
        fail_if_exists: bool = False,
    ):
        if not filename:
            filename = os.path.basename(path)

        obj = self.exists(filename)

        with open(path, "rb") as f:
            content = f.read()
            file_md5 = hashlib.md5(content).hexdigest()

        # check if the object already exists
        if obj:
            if file_md5 == obj["ETag"].replace('"', "") or file_md5 == obj[
                "Metadata"
            ].get("md5", ""):
                # the same object already exists
                return True
            elif fail_if_exists:
                # explicitly raise error for duplicated filename
                raise Exception(
                    "file {} already exists with different contents".format(filename)
                )

        options: Dict[str, Any] = {
            "Bucket": self.bucket,
            "Key": self.full_path(filename),
            "ACL": self.access_policy,
            "ContentType": content_type,
            "Metadata": {"md5": file_md5},
        }
        if cache_control:
            options["CacheControl"] = cache_control

        if self.encryption:
            options["ServerSideEncryption"] = "AES256"

        with open(path, "rb") as f:
            options["Body"] = f
            try:
                self.client.put_object(**options)
                return True
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    return False
                else:
                    raise
