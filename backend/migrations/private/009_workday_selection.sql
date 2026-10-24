CREATE TABLE workday_selections (
 workday_id uuid PRIMARY KEY REFERENCES workdays(id) ON DELETE CASCADE,
 activity_id uuid NOT NULL,
 revision integer NOT NULL CHECK (revision > 0)
);
CREATE TABLE workday_selection_operations (
 id uuid PRIMARY KEY,
 owner uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
 workday_id uuid NOT NULL REFERENCES workdays(id) ON DELETE CASCADE,
 payload_hash text NOT NULL,
 result jsonb NOT NULL,
 expires_at timestamptz NOT NULL
);
CREATE INDEX workday_selection_operations_owner ON workday_selection_operations(owner);
CREATE TABLE workday_lifecycles (
 workday_id uuid PRIMARY KEY REFERENCES workdays(id) ON DELETE CASCADE,
 state text NOT NULL CHECK (state = 'active'),
 started_at timestamptz NOT NULL,
 revision integer NOT NULL CHECK (revision = 1)
);
CREATE TABLE workday_start_operations (
 id uuid PRIMARY KEY,
 owner uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
 workday_id uuid NOT NULL REFERENCES workdays(id) ON DELETE CASCADE,
 payload_hash text NOT NULL,
 result jsonb NOT NULL,
 expires_at timestamptz NOT NULL
);
CREATE INDEX workday_start_operations_owner ON workday_start_operations(owner);
