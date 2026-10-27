-- Runs only on a NEW tablet volume. Never apply to the ordinary database.
-- Read the application password inside PostgreSQL; no shell/SQL interpolation.
DO $$
DECLARE application_password text;
BEGIN
    application_password := btrim(pg_read_file('/run/secrets/tablet_postgres_password'));
    IF length(application_password) < 32 THEN
        RAISE EXCEPTION 'Application secret missing or too short';
    END IF;
    EXECUTE format('CREATE ROLE private_work LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION PASSWORD %L', application_password);
END
$$;
ALTER DATABASE private_work OWNER TO private_work;
