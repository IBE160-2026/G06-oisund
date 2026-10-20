-- Content-free acknowledgements survive the draft/operations cascade only until
-- the original draft deadline, so an authorized lost reply can be settled.
CREATE TABLE draft_deletions (
 id uuid PRIMARY KEY,
 owner uuid NOT NULL REFERENCES accounts(id),
 draft_id uuid NOT NULL,
 expected_revision integer NOT NULL CHECK (expected_revision > 0),
 expires_at timestamptz NOT NULL
);
CREATE INDEX draft_deletions_expiry ON draft_deletions(expires_at);
