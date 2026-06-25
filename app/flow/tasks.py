from prefect import task, get_run_logger
from dataclasses import dataclass
from datetime import datetime

from app.services.client import get_clickhouse_client, get_repo_handle

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

@task
def get_sync_state(repo_name : str):
    log = get_run_logger()

    client = get_clickhouse_client()

    try:
        result = client.query(
            f"SELECT last_synced_at, last_synced_sha FROM sync_state WHERE repo = {repo_name}"
        )

        if result.result_rows:
            last_synced_at, last_synced_sha = result.result_rows[0]
        else:
            last_synced_at, last_synced_sha = None, None

        return (last_synced_at,last_synced_sha)

    finally:
        client.close()

@task(retries=3, retry_delay_seconds=[10, 30, 90])
def fetch_commits(repo_name : str, since_datetime : datetime):

    client = get_clickhouse_client()

    repo_handle = get_repo_handle(client, repo_name)

    commits = repo_handle.get_commits(since=since_datetime)