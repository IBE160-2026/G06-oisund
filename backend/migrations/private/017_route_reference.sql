ALTER TABLE workday_operations ADD COLUMN route_revision integer CHECK (route_revision >= 0);

CREATE TABLE draft_route_decisions (
 draft_id uuid NOT NULL REFERENCES drafts(id) ON DELETE CASCADE,
 revision integer NOT NULL CHECK (revision > 0),
 draft_revision integer NOT NULL CHECK (draft_revision > 0),
 activity_id uuid NOT NULL,
 operation_id uuid NOT NULL UNIQUE,
 payload_hash text NOT NULL,
 reference jsonb,
 PRIMARY KEY (draft_id, revision)
);
CREATE INDEX draft_route_decisions_by_activity ON draft_route_decisions(draft_id, activity_id, revision DESC);

CREATE TABLE workday_route_references (
 workday_id uuid NOT NULL REFERENCES workdays(id) ON DELETE CASCADE,
 activity_id uuid NOT NULL,
 reference jsonb NOT NULL,
 PRIMARY KEY (workday_id, activity_id)
);
