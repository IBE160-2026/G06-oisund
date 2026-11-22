CREATE TABLE public_road_area_versions (
    effective_date date NOT NULL,
    area_id text NOT NULL,
    observed_at timestamptz NOT NULL,
    checked_at timestamptz NOT NULL,
    source_sha256 text NOT NULL,
    revision text NOT NULL,
    source jsonb NOT NULL CHECK (jsonb_typeof(source) = 'object'),
    manifest jsonb NOT NULL CHECK (jsonb_typeof(manifest) = 'object'),
    PRIMARY KEY (effective_date, area_id, observed_at, checked_at),
    CHECK (area_id IN ('kvaloya', 'tromsoya', 'fastlandet')),
    CHECK (source_sha256 ~ '^[a-f0-9]{64}$' AND revision ~ '^[a-f0-9]{64}$'),
    CHECK (checked_at >= observed_at)
);
