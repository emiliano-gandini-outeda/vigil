-- upgrade

CREATE TABLE IF NOT EXISTS commits (
    repo String NOT NULL,
    sha String NOT NULL,
    author_login String NOT NULL,
    author_name String NOT NULL,
    author_email String NOT NULL,
    message String,
    committed_at DateTime64(3) NOT NULL
)
ENGINE = MergeTree()
ORDER BY (repo, committed_at)
PRIMARY KEY repo

CREATE TABLE IF NOT EXISTS repos (
    name String NOT NULL,
    owner String NOT NULL,
    is_org Bool NOT NULL,
    default_branch String NOT NULL
)
ENGINE = ReplacingMergeTree()
ORDER BY (name)
PRIMARY KEY name

CREATE TABLE IF NOT EXISTS sync_state (
    repo String NOT NULL,
    last_synced_sha String NOT NULL,
    last_synced_at DateTime64(3) NOT NULL,
    last_run_status String NOT NULL,
    last_run_at DateTime64(3) NOT NULL
)
ENGINE = ReplacingMergeTree()
ORDER BY (repo)
PRIMARY KEY repo

-- rollback

DROP TABLE sync_state

DROP TABLE repos

DROP TABLE commits
