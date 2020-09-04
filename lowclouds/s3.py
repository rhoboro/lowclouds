from typing import Optional

import boto3


def put_object(filename: str, uri: str) -> str:
    """S3にファイルをアップロードする

    :param uri: アップロード先のフォルダのURI。s3://...の文字列
    :param filename: 元のファイルパス。Noneならbytesで返す。
    :return アップロード先のuri
    """
    s3 = boto3.resource("s3")
    if not uri.startswith("s3://"):
        raise ValueError("uri needs to start with s3://")

    bucket_name, object_path = (uri[5:]).split("/", 1)
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(filename, object_path)
    return uri


def get_object(uri: str, filename: str = None) -> Optional[bytes]:
    """S3からオブジェクトを取得する

    :param uri: 取得元のオブジェクトのURI。s3://...の文字列
    :param filename: 保存先のファイルパス。Noneならbytesで返す。
    :return: オブジェクトの中身。filenameが与えられたときはNone
    """
    s3 = boto3.client("s3")
    if not uri.startswith("s3://"):
        raise ValueError("uri needs to start with s3://")

    bucket_name, object_path = (uri[5:]).split("/", 1)
    if filename:
        with open(filename, "wb") as f:
            f.write(s3.get_object(Bucket=bucket_name, Key=object_path)["Body"].read())
        return None
    else:
        return s3.get_object(Bucket=bucket_name, Key=object_path)["Body"].read()
