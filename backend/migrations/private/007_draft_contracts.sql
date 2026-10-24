-- Pin existing receipts/reviews to original semantics without rewriting facts.
ALTER TABLE draft_operations ADD COLUMN IF NOT EXISTS normalize_physical_bus boolean NOT NULL DEFAULT false;
ALTER TABLE workday_operations ADD COLUMN IF NOT EXISTS assessment_policy_version integer NOT NULL DEFAULT 1 CHECK (assessment_policy_version IN (1,2));
ALTER TABLE workdays ADD COLUMN IF NOT EXISTS assessment_policy_version integer NOT NULL DEFAULT 1 CHECK (assessment_policy_version IN (1,2));
