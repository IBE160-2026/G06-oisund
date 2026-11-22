-- The single anchor and compact retry receipts inherit the parent deadline.
-- Cascading from workdays handles both explicit deletion and expiry cleanup.
CREATE TABLE workday_position_anchors (
 workday_id uuid PRIMARY KEY REFERENCES workdays(id) ON DELETE CASCADE,
 activity_id uuid NOT NULL,
 revision integer NOT NULL CHECK (revision > 0),
 route_revision integer NOT NULL CHECK (route_revision > 0),
 route_basis text NOT NULL CHECK (route_basis ~ '^[a-f0-9]{64}$'),
 source_version varchar(200) NOT NULL,
 coordinate_revision varchar(100),
 mapping_revision varchar(100),
 quay_version varchar(100),
 stop_place_version varchar(100),
 service_date date NOT NULL,
 journey_id varchar(200) NOT NULL,
 pattern_id varchar(200) NOT NULL,
 occurrence_id varchar(200) NOT NULL,
 quay_id varchar(40) NOT NULL,
 stop_place_id varchar(40) NOT NULL,
 origin text NOT NULL CHECK (origin IN ('manual', 'gps')),
 evidence_at timestamptz NOT NULL,
 asserted_at timestamptz,
 saved_at timestamptz NOT NULL,
 CHECK ((origin = 'manual') = (asserted_at IS NOT NULL))
);

CREATE TABLE workday_position_anchor_operations (
 id uuid PRIMARY KEY,
 workday_id uuid NOT NULL REFERENCES workdays(id) ON DELETE CASCADE,
 payload_hash text NOT NULL CHECK (payload_hash ~ '^[a-f0-9]{64}$'),
 anchor_revision integer NOT NULL CHECK (anchor_revision > 0),
 accepted_at timestamptz NOT NULL
);
CREATE INDEX workday_position_anchor_operations_parent ON workday_position_anchor_operations(workday_id);
