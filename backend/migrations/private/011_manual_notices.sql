CREATE TABLE workday_notices (
    id uuid PRIMARY KEY,
    workday_id uuid NOT NULL REFERENCES workdays(id) ON DELETE CASCADE,
    revision integer NOT NULL CHECK (revision > 0),
    title text NOT NULL CHECK (length(title) BETWEEN 1 AND 300),
    line_tags jsonb NOT NULL CHECK (jsonb_typeof(line_tags)='array' AND jsonb_array_length(line_tags) BETWEEN 1 AND 50),
    source_url text NOT NULL CHECK (length(source_url) BETWEEN 1 AND 2048),
    source_updated_at timestamptz,
    valid_from timestamptz,
    valid_until timestamptz,
    status text NOT NULL CHECK (status IN ('registered','ended_manually')),
    entered_at timestamptz NOT NULL,
    edited_at timestamptz NOT NULL,
    checked_at timestamptz,
    checked_revision integer,
    CHECK (valid_from IS NULL OR valid_until IS NULL OR valid_from <= valid_until),
    CHECK ((checked_at IS NULL AND checked_revision IS NULL) OR (checked_at IS NOT NULL AND checked_revision IS NOT NULL AND checked_revision BETWEEN 1 AND revision))
);
CREATE INDEX workday_notices_parent ON workday_notices(workday_id,id);
CREATE TABLE workday_notice_operations (
    id uuid PRIMARY KEY,
    owner uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    workday_id uuid NOT NULL REFERENCES workdays(id) ON DELETE CASCADE,
    payload_hash text NOT NULL,
    result jsonb NOT NULL,
    expires_at timestamptz NOT NULL
);
CREATE INDEX workday_notice_operations_owner ON workday_notice_operations(owner,expires_at);
