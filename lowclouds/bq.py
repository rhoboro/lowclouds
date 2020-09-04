from functools import lru_cache

from google.cloud.bigquery import Client
from google.cloud.bigquery.job import QueryJobConfig, WriteDisposition


@lru_cache()
def _get_client(project: str = None) -> Client:
    return Client(project=project)


def query(
    sql: str,
    destination_dataset: str = None,
    destination_table: str = None,
    project: str = None,
    timeout: int = None,
    append: bool = False,
) -> str:
    """クエリを実行します"""

    client = _get_client(project)
    if not (destination_dataset and destination_table):
        return client.query(sql).result(timeout=timeout)

    dataset = client.get_dataset(destination_dataset)
    table = dataset.table(destination_table)
    disposition = WriteDisposition.WRITE_APPEND if append else WriteDisposition.WRITE_TRUNCATE
    job_config = QueryJobConfig(destination=table, write_disposition=disposition)
    query_job = client.query(sql, job_config=job_config)
    return query_job.result(timeout=timeout)
