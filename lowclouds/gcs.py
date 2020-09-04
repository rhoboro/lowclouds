from functools import lru_cache
from typing import Optional

from google.cloud.storage import Client


@lru_cache()
def _get_client(project: str = None) -> Client:
    return Client(project=project)


def put_object(filename: str, uri: str, project: str = None) -> str:
    """GCSにファイルをアップロードする

    :param uri: アップロード先のフォルダのURI。gs://...の文字列
    :param filename: 元のファイルパス。Noneならbytesで返す。
    :param project: プロジェクトID
    :return アップロード先のuri
    """
    client = _get_client(project)
    if not uri.startswith("gs://"):
        raise ValueError("uri needs to start with gs://")

    bucket_name, blob_name = uri[5:].split("/", 1)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(filename=filename)
    return uri


def get_object(uri: str, filename: str = None, project: str = None) -> Optional[bytes]:
    """GCSからオブジェクトを取得する

    :param uri: 取得元のオブジェクトのURI。gs://...の文字列
    :param filename: 保存先のファイルパス。Noneならbytesで返す。
    :param project: プロジェクトID
    :return: オブジェクトの中身。filenameが与えられたときはNone
    """
    client = _get_client(project)
    if not uri.startswith("gs://"):
        raise ValueError("uri needs to start with gs://")

    bucket_name, blob_name = uri[5:].split("/", 1)
    data = client.bucket(bucket_name).get_blob(blob_name)
    if not data:
        raise ValueError("cannot get any data")

    if filename:
        data.download_to_filename(filename)
        return None
    else:
        return data.download_as_string()
