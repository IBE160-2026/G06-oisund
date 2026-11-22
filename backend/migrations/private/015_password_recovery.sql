CREATE TABLE recovery_proofs (
    id uuid PRIMARY KEY,
    owner uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    purpose text NOT NULL DEFAULT 'password-recovery' CHECK (purpose = 'password-recovery'),
    digest text NOT NULL UNIQUE CHECK (digest ~ '^[0-9a-f]{64}$'),
    state text NOT NULL DEFAULT 'active' CHECK (state IN ('active','revoked','consumed')),
    created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
    expires_at timestamptz NOT NULL,
    CHECK (expires_at > created_at AND expires_at <= created_at + interval '30 minutes')
);
CREATE UNIQUE INDEX recovery_one_active ON recovery_proofs(owner) WHERE state='active';
CREATE INDEX recovery_expiry ON recovery_proofs(expires_at);
CREATE TABLE recovery_audit (
    id bigserial PRIMARY KEY,
    owner uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    actor text NOT NULL CHECK (length(actor) BETWEEN 1 AND 200),
    action text NOT NULL CHECK (action IN ('issue','revoke','delivery','change')),
    result text NOT NULL CHECK (result IN ('issued','revoked','limited','failed','acknowledged')),
    occurred_at timestamptz NOT NULL DEFAULT clock_timestamp()
);
CREATE INDEX recovery_audit_owner_time ON recovery_audit(owner,occurred_at);
