-- Optional applicability, independent of source text and storage retention.
ALTER TABLE workday_notices ADD COLUMN geography jsonb
    CHECK (geography IS NULL OR jsonb_typeof(geography) = 'object');
