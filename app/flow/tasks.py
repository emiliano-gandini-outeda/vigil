from prefect import task, get_run_logger
from dataclasses import dataclass

from app.services.client import get_clickhouse_client

@dataclass(frozen=True)
class RepoRecord:
    full_name: str
    default_branch: str

@task
def load_active_repos():
    log = get_run_logger()

    client = get_clickhouse_client()

    try:
        result = client.query(
            "SELECT name, default_branch FROM repos"
        )
    
    finally:
        client.close()
    
    repos = [RepoRecord(name=row[0], default_branch=row[1]) for row in result.result_rows]
    
    log.info(f"Loaded {len(repos)} active repos")
    return repos