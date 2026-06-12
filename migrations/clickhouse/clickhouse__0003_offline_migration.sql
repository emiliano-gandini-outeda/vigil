-- upgrade

-- ch_projections change for commits requires manual migration
ALTER TABLE commits MODIFY ORDER BY (repo, committed_at)

-- ch_projections change for repos requires manual migration

-- rollback

-- ch_projections change for commits requires manual migration
ALTER TABLE commits MODIFY ORDER BY (repo, commited_at)

-- ch_projections change for repos requires manual migration
