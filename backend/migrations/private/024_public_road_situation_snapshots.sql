CREATE TABLE public_road_situation_snapshots (
    observed_at timestamptz PRIMARY KEY,
    sha256 text NOT NULL CHECK (sha256 ~ '^[a-f0-9]{64}$'),
    source_url text NOT NULL,
    events jsonb NOT NULL CHECK (jsonb_typeof(events) = 'array')
);
