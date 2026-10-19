CREATE TABLE IF NOT EXISTS schema_migrations (version integer PRIMARY KEY);
CREATE TABLE IF NOT EXISTS creation_operations (
  id uuid PRIMARY KEY,
  owner text NOT NULL CHECK (owner = 'fictional-assessment-owner'),
  created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  expires_at timestamptz NOT NULL DEFAULT clock_timestamp() + interval '7 days'
);
CREATE TABLE IF NOT EXISTS fictional_days (
  id uuid PRIMARY KEY,
  operation_id uuid NOT NULL UNIQUE REFERENCES creation_operations(id) ON DELETE CASCADE,
  owner text NOT NULL CHECK (owner = 'fictional-assessment-owner'),
  payload jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  expires_at timestamptz NOT NULL DEFAULT clock_timestamp() + interval '7 days'
);
INSERT INTO schema_migrations VALUES (1) ON CONFLICT DO NOTHING;
