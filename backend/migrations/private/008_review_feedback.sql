-- Preserve every historical policy value; widen only the allowed versions.
ALTER TABLE workday_operations DROP CONSTRAINT workday_operations_assessment_policy_version_check;
ALTER TABLE workday_operations ADD CONSTRAINT workday_operations_assessment_policy_version_check CHECK (assessment_policy_version IN (1,2,3));
ALTER TABLE workdays DROP CONSTRAINT workdays_assessment_policy_version_check;
ALTER TABLE workdays ADD CONSTRAINT workdays_assessment_policy_version_check CHECK (assessment_policy_version IN (1,2,3));
