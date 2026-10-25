-- Preserve existing snapshots and first starts; terminal retention only shortens.
ALTER TABLE workdays DROP CONSTRAINT workdays_check;
ALTER TABLE workdays ADD CONSTRAINT workdays_retention CHECK (expires_at <= final_end + interval '7 days');
ALTER TABLE workday_lifecycles DROP CONSTRAINT workday_lifecycles_state_check;
ALTER TABLE workday_lifecycles DROP CONSTRAINT workday_lifecycles_revision_check;
ALTER TABLE workday_lifecycles ADD COLUMN ended_at timestamptz;
ALTER TABLE workday_lifecycles ADD CONSTRAINT lifecycle_state CHECK (
 (state='active' AND revision=1 AND ended_at IS NULL) OR
 (state IN ('ended','aborted') AND revision=2 AND ended_at IS NOT NULL AND ended_at>=started_at));
CREATE TABLE workday_outcome_revisions (
 workday_id uuid PRIMARY KEY REFERENCES workdays(id) ON DELETE CASCADE,
 revision integer NOT NULL CHECK (revision>0)
);
CREATE TABLE workday_outcomes (
 workday_id uuid NOT NULL REFERENCES workdays(id) ON DELETE CASCADE,
 activity_id uuid NOT NULL,
 outcome text NOT NULL CHECK (outcome IN ('unregistered','completed','skipped','interrupted')),
 PRIMARY KEY(workday_id,activity_id)
);
CREATE TABLE workday_outcome_operations (
 id uuid PRIMARY KEY, owner uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
 workday_id uuid NOT NULL REFERENCES workdays(id) ON DELETE CASCADE,
 payload_hash text NOT NULL, result jsonb NOT NULL, expires_at timestamptz NOT NULL
);
CREATE INDEX workday_outcome_operations_owner ON workday_outcome_operations(owner);
CREATE TABLE workday_close_operations (
 id uuid PRIMARY KEY, owner uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
 workday_id uuid NOT NULL REFERENCES workdays(id) ON DELETE CASCADE,
 payload_hash text NOT NULL, result jsonb NOT NULL, expires_at timestamptz NOT NULL
);
CREATE INDEX workday_close_operations_owner ON workday_close_operations(owner);
