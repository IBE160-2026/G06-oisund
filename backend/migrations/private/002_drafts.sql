CREATE TABLE drafts (
 id uuid PRIMARY KEY,
 owner uuid NOT NULL REFERENCES accounts(id),
 created_at timestamptz NOT NULL DEFAULT statement_timestamp(),
 expires_at timestamptz NOT NULL DEFAULT statement_timestamp() + interval '7 days',
 revision integer NOT NULL CHECK (revision > 0),
 content jsonb NOT NULL,
 CHECK (expires_at = created_at + interval '7 days')
);
CREATE INDEX drafts_owner ON drafts(owner);
CREATE INDEX drafts_expiry ON drafts(expires_at);
CREATE TABLE draft_operations (
 id uuid PRIMARY KEY,
 owner uuid NOT NULL REFERENCES accounts(id),
 draft_id uuid REFERENCES drafts(id) ON DELETE CASCADE,
 expires_at timestamptz NOT NULL DEFAULT statement_timestamp() + interval '7 days',
 payload_hash text,
 result jsonb,
 CHECK ((payload_hash IS NULL) = (result IS NULL))
);
CREATE INDEX draft_operations_expiry ON draft_operations(expires_at);
