-- An older/conflicting revision can prove identity membership without observing
-- the current revision. Retain the last complete identity membership on upgrade.
CREATE TABLE automatic_notice_identities (
 participant text NOT NULL,
 situation text NOT NULL,
 last_seen timestamptz NOT NULL,
 last_complete_generation uuid,
 PRIMARY KEY (participant,situation)
);
CREATE INDEX automatic_notice_identity_generation ON automatic_notice_identities(last_complete_generation);
CREATE INDEX automatic_notice_identity_expiry ON automatic_notice_identities(last_seen);

INSERT INTO automatic_notice_identities(participant,situation,last_seen,last_complete_generation)
 SELECT source.participant,source.situation,max(source.last_seen),
        CASE WHEN bool_or(source.last_complete_generation=feed.generation) THEN feed.generation END
 FROM automatic_notice_sources AS source CROSS JOIN automatic_notice_feed AS feed
 GROUP BY source.participant,source.situation,feed.generation;

-- Legacy writes could mark two revisions in one completed cycle; the old state
-- cannot reliably recover which was sent. Drop older unverifiable generation
-- claims too. The content, observation clocks and private receipts stay intact.
WITH ambiguous AS (
 SELECT participant,situation,last_complete_generation
 FROM automatic_notice_sources
 WHERE last_complete_generation IS NOT NULL
 GROUP BY participant,situation,last_complete_generation HAVING count(*)>1
)
UPDATE automatic_notice_sources AS source SET last_complete_generation=NULL
 WHERE source.last_complete_generation IS NOT NULL AND (
  source.last_complete_generation IS DISTINCT FROM (SELECT generation FROM automatic_notice_feed)
  OR EXISTS (SELECT 1 FROM ambiguous AS item WHERE (item.participant,item.situation,item.last_complete_generation)
             =(source.participant,source.situation,source.last_complete_generation))
 );
