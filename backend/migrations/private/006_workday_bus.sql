CREATE TABLE workday_buses (
 workday_id uuid PRIMARY KEY REFERENCES workdays(id) ON DELETE CASCADE,
 physical_bus text CHECK (physical_bus IS NULL OR length(physical_bus) <= 100),
 revision integer NOT NULL CHECK (revision > 0)
);
CREATE TABLE workday_bus_operations (
 id uuid PRIMARY KEY,
 owner uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
 workday_id uuid NOT NULL REFERENCES workdays(id) ON DELETE CASCADE,
 payload_hash text NOT NULL,
 result jsonb NOT NULL,
 expires_at timestamptz NOT NULL
);
CREATE INDEX workday_bus_operations_owner ON workday_bus_operations(owner);
