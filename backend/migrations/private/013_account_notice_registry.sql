-- One canonical incident; workday_id is optional provenance, never ownership.
ALTER TABLE workday_notices ADD COLUMN owner uuid REFERENCES accounts(id) ON DELETE CASCADE,
 ADD COLUMN expires_at timestamptz, ADD COLUMN ended_at timestamptz;
UPDATE workday_notices n SET owner=w.owner,
 expires_at=CASE
 WHEN n.status='ended_manually' THEN GREATEST(n.edited_at+interval '7 days',clock_timestamp()+interval '7 days')
 WHEN n.valid_until IS NULL THEN w.expires_at
 WHEN n.valid_until<=clock_timestamp() THEN GREATEST(n.valid_until+interval '7 days',clock_timestamp()+interval '7 days')
 ELSE n.valid_until+interval '7 days' END
 FROM workdays w WHERE w.id=n.workday_id;
ALTER TABLE workday_notices ALTER COLUMN owner SET NOT NULL, ALTER COLUMN expires_at SET NOT NULL,
 ALTER COLUMN workday_id DROP NOT NULL, DROP CONSTRAINT workday_notices_workday_id_fkey;
ALTER TABLE workday_notices ADD FOREIGN KEY(workday_id) REFERENCES workdays(id) ON DELETE SET NULL;
CREATE INDEX account_notices_owner ON workday_notices(owner,id);
ALTER TABLE workday_notice_operations ALTER COLUMN workday_id DROP NOT NULL,
 DROP CONSTRAINT workday_notice_operations_workday_id_fkey;
ALTER TABLE workday_notice_operations ADD FOREIGN KEY(workday_id) REFERENCES workdays(id) ON DELETE SET NULL;
UPDATE workday_notice_operations o SET expires_at=n.expires_at
 FROM workday_notices n WHERE o.result->>'id'=n.id::text;
CREATE TABLE account_notice_operations (
 id uuid PRIMARY KEY, owner uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
 notice_id uuid NOT NULL REFERENCES workday_notices(id) ON DELETE CASCADE,
 payload_hash text NOT NULL, result jsonb NOT NULL, expires_at timestamptz NOT NULL
);
CREATE INDEX account_notice_operations_owner ON account_notice_operations(owner,expires_at);
