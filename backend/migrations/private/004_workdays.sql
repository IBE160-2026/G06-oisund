-- Snapshots deliberately have no foreign key to their disposable source draft.
ALTER TABLE drafts ADD COLUMN confirmed boolean NOT NULL DEFAULT false;
CREATE TABLE workdays (
 id uuid PRIMARY KEY,
 owner uuid NOT NULL REFERENCES accounts(id),
 source_draft_id uuid NOT NULL UNIQUE,
 source_revision integer NOT NULL CHECK (source_revision > 0),
 confirmed_at timestamptz NOT NULL DEFAULT statement_timestamp(),
 final_end timestamptz NOT NULL,
 expires_at timestamptz NOT NULL,
 content jsonb NOT NULL,
 acknowledgements jsonb NOT NULL,
 classifications jsonb NOT NULL,
 CHECK (expires_at = final_end + interval '7 days')
);
CREATE INDEX workdays_owner ON workdays(owner, id);
CREATE INDEX workdays_expiry ON workdays(expires_at);
CREATE TABLE workday_operations (
 id uuid PRIMARY KEY,
 owner uuid NOT NULL REFERENCES accounts(id),
 draft_id uuid NOT NULL,
 expected_revision integer NOT NULL CHECK (expected_revision > 0),
 expires_at timestamptz NOT NULL,
 payload_hash text,
 workday_id uuid REFERENCES workdays(id) ON DELETE CASCADE,
 CHECK ((payload_hash IS NULL) = (workday_id IS NULL))
);
CREATE INDEX workday_operations_expiry ON workday_operations(expires_at);
CREATE INDEX workday_operations_draft ON workday_operations(draft_id);
