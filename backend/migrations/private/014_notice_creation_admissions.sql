-- Payload-free bounded admission; accepted commands use immutable receipts.
CREATE TABLE notice_creation_admissions (
    id uuid PRIMARY KEY,
    owner uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    expires_at timestamptz NOT NULL
);
CREATE INDEX notice_creation_admissions_owner ON notice_creation_admissions(owner);
CREATE INDEX notice_creation_admissions_expiry ON notice_creation_admissions(expires_at);
