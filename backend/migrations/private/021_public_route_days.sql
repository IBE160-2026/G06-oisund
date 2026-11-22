CREATE TABLE public_route_days (
    service_date date NOT NULL,
    line_code text NOT NULL,
    observed_at timestamptz NOT NULL,
    provenance jsonb NOT NULL CHECK (jsonb_typeof(provenance) = 'object'),
    journeys jsonb NOT NULL CHECK (jsonb_typeof(journeys) = 'object'),
    PRIMARY KEY (service_date, line_code)
);
