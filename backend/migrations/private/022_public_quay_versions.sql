CREATE TABLE public_quay_versions (
    revision text NOT NULL,
    quay_id text NOT NULL,
    source jsonb NOT NULL CHECK (jsonb_typeof(source) = 'object'),
    record jsonb NOT NULL CHECK (jsonb_typeof(record) = 'object'),
    PRIMARY KEY (revision, quay_id)
);
