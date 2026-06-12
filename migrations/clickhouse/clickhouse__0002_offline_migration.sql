-- upgrade

CREATE TABLE IF NOT EXISTS repos (
    name String NOT NULL,
    owner String NOT NULL,
    is_org Bool NOT NULL,
    default_branch String NOT NULL
)
ENGINE = ReplacingMergeTree()
ORDER BY (name)
PRIMARY KEY name

DROP TABLE repo

-- rollback

DROP TABLE repos

CREATE TABLE repo (/* see .dbwarden/schemas/ for DDL */)
