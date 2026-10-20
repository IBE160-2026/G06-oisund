CREATE TABLE accounts (
 id uuid PRIMARY KEY, username text UNIQUE NOT NULL, password_hash text NOT NULL
);
CREATE TABLE sessions (
 token_hash text PRIMARY KEY, owner uuid NOT NULL REFERENCES accounts(id),
 created_at timestamptz NOT NULL DEFAULT statement_timestamp(),
 expires_at timestamptz NOT NULL DEFAULT statement_timestamp() + interval '14 days',
 CHECK (expires_at = created_at + interval '14 days')
);
CREATE INDEX sessions_expiry ON sessions(expires_at);
CREATE TABLE login_limits (
 bucket text PRIMARY KEY, attempts integer NOT NULL,
 expires_at timestamptz NOT NULL
);
CREATE TABLE security_settings (id integer PRIMARY KEY CHECK(id=1), csrf_key text NOT NULL);
