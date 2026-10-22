-- Content-free receipts survive deletion only until the original plan deadline.
CREATE TABLE workday_deletions (
 id uuid PRIMARY KEY,
 owner uuid NOT NULL REFERENCES accounts(id),
 workday_id uuid NOT NULL,
 source_revision integer NOT NULL CHECK (source_revision > 0),
 expires_at timestamptz NOT NULL
);
CREATE INDEX workday_deletions_expiry ON workday_deletions(expires_at);
