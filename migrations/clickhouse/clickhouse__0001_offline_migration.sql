-- upgrade

CREATE TABLE IF NOT EXISTS commits (
    author_email String NOT NULL,
    author_login String NOT NULL,
    author_name String NOT NULL,
    committed_at DateTime64(3) NOT NULL,
    message String,
    repo NULL NOT NULL REFERENCES repos(name),
    sha String NOT NULL
)
ENGINE = MergeTree()
ORDER BY (repo, committed_at)
PRIMARY KEY repo

CREATE TABLE IF NOT EXISTS repos (
    default_branch String NOT NULL,
    is_org Bool NOT NULL,
    name String NOT NULL,
    owner String NOT NULL
)
ENGINE = ReplacingMergeTree()
ORDER BY (name)
PRIMARY KEY name

-- rollback

DROP TABLE commits

DROP TABLE repos
