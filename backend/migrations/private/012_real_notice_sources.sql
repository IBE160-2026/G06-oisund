-- Add source text and explicit scope without rewriting historical receipts.
ALTER TABLE workday_notices
    ADD COLUMN summary text CHECK (length(summary) BETWEEN 1 AND 1000),
    ADD COLUMN description text CHECK (length(description) BETWEEN 1 AND 5000),
    ADD COLUMN source_note text CHECK (length(source_note) BETWEEN 1 AND 500),
    ADD COLUMN line_scope text NOT NULL DEFAULT 'selected' CHECK (line_scope IN ('selected','all')),
    ALTER COLUMN source_url DROP NOT NULL,
    DROP CONSTRAINT workday_notices_line_tags_check;
ALTER TABLE workday_notices ADD CONSTRAINT workday_notices_line_tags_check CHECK (
    jsonb_typeof(line_tags)='array' AND jsonb_array_length(line_tags) <= 50
    AND ((line_scope='selected' AND jsonb_array_length(line_tags)>0)
         OR (line_scope='all' AND jsonb_array_length(line_tags)=0))
);
