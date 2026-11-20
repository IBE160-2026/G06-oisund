-- Entur TRO is the only source in this pilot. No account data enters these tables.
CREATE TABLE automatic_notice_feed (
 id boolean PRIMARY KEY DEFAULT true CHECK (id),
 status text NOT NULL DEFAULT 'never-qualified' CHECK (status IN ('never-qualified','collecting','complete','partial','unavailable')),
 attempt_at timestamptz,
 result_at timestamptz,
 generation uuid,
 baseline_at timestamptz,
 synchronized_at timestamptz,
 baseline_count integer CHECK (baseline_count >= 0),
 response_at timestamptz,
 attempt_pages integer NOT NULL DEFAULT 0 CHECK (attempt_pages >= 0),
 attempt_count integer NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
 failure text,
 next_request_at timestamptz NOT NULL DEFAULT '-infinity',
 CONSTRAINT automatic_notice_baseline_complete CHECK (
   (generation IS NULL AND baseline_at IS NULL AND synchronized_at IS NULL AND baseline_count IS NULL) OR
   (generation IS NOT NULL AND baseline_at IS NOT NULL AND synchronized_at IS NOT NULL AND baseline_count IS NOT NULL))
);
INSERT INTO automatic_notice_feed DEFAULT VALUES;

CREATE TABLE automatic_notice_sources (
 participant text NOT NULL,
 situation text NOT NULL,
 revision text NOT NULL CHECK (length(revision) = 64),
 content jsonb NOT NULL,
 first_seen timestamptz NOT NULL,
 last_seen timestamptz NOT NULL,
 fetched_at timestamptz NOT NULL,
 response_at timestamptz NOT NULL,
 last_complete_generation uuid,
 current_revision boolean NOT NULL,
 conflicting boolean NOT NULL DEFAULT false,
 superseded_at timestamptz,
 PRIMARY KEY (participant,situation,revision)
);
CREATE UNIQUE INDEX automatic_notice_current_source ON automatic_notice_sources(participant,situation) WHERE current_revision;
CREATE INDEX automatic_notice_source_expiry ON automatic_notice_sources(last_seen);

-- The workday's authoritative deadline can shorten on closure. The composite key
-- propagates that deadline to every private copy and cascades parent removal.
ALTER TABLE workdays ADD CONSTRAINT automatic_notice_workday_parent UNIQUE (id,owner,expires_at);
CREATE TABLE automatic_notice_reviews (
 workday_id uuid NOT NULL,
 owner uuid NOT NULL,
 expires_at timestamptz NOT NULL,
 participant text NOT NULL,
 situation text NOT NULL,
 revision integer NOT NULL CHECK (revision > 0),
 decision jsonb NOT NULL,
 PRIMARY KEY (workday_id,participant,situation),
 FOREIGN KEY (workday_id,owner,expires_at) REFERENCES workdays(id,owner,expires_at) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE automatic_notice_review_operations (
 id uuid NOT NULL,
 workday_id uuid NOT NULL,
 owner uuid NOT NULL,
 expires_at timestamptz NOT NULL,
 payload_hash text NOT NULL CHECK (length(payload_hash) = 64),
 result jsonb NOT NULL,
 PRIMARY KEY (workday_id,id),
 FOREIGN KEY (workday_id,owner,expires_at) REFERENCES workdays(id,owner,expires_at) ON UPDATE CASCADE ON DELETE CASCADE
);
