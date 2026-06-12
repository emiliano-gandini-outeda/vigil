-- upgrade

CREATE TABLE IF NOT EXISTS repo (
    name String NOT NULL,
    owner String NOT NULL,
    is_org Bool NOT NULL,
    default_branch String NOT NULL
)
ENGINE = ReplacingMergeTree()
ORDER BY (name)
PRIMARY KEY name

-- rollback

DROP TABLE repo
