from prefect import task, get_run_logger
from dataclasses import dataclass
from datetime import datetime
from github import RateLimitExceededException
from prefect.tasks import exponential_backoff

from app.services.client import get_clickhouse_client, get_repo_handle, github_session
from app.services.commits import extract_commit_data
from app.models.commit import Commit

@dataclass(frozen=True)
class RepoRecord:
    name: str
    owner: str
    default_branch: str

@task
def load_active_repos():
    log = get_run_logger()

    client = get_clickhouse_client()

    try:
        result = client.query(
            "SELECT name, owner, default_branch FROM repos"
        )
    
    finally:
        client.close()
    
    repos = [RepoRecord(name=row[0], owner=row[1], default_branch=row[2]) for row in result.result_rows]
    
    log.info(f"Loaded {len(repos)} active repos")
    return repos

@task
def get_sync_state(repo_name : str):

    client = get_clickhouse_client()

    try:
        result = client.query(
            "SELECT last_synced_at, last_synced_sha FROM sync_state WHERE repo = %(repo)s",
            parameters={"repo": repo_name},
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

    log = get_run_logger()

    with github_session() as gh:
        try:
            repo_handle = get_repo_handle(gh, repo_name)

            if since_datetime is None:
                commits = repo_handle.get_commits()
            else:
                commits = repo_handle.get_commits(since=since_datetime)

            results = []

            for commit in commits:
                results.append(extract_commit_data(commit))

            log.info(f"{repo_name} -> {len(results)} commits fetched (since={since_datetime})")
            return results
        
        except RateLimitExceededException:
            reset_time = gh.get_rate_limit().core.reset
            log.warning(f"Rate limit hit for {repo_name}, resets at {reset_time}: letting Prefect retry")
            raise

