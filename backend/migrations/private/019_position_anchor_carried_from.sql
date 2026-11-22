-- Keep the original anchor migration usable by existing V2 sandboxes.
ALTER TABLE workday_position_anchors ADD COLUMN IF NOT EXISTS carried_from jsonb;
