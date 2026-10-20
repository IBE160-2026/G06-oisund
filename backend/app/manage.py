import sys
import getpass
import os
from .storage import cleanup, database, migrate
from .main import create_day, operation
from .domain import CreateDay, FIXTURE


def seed():
    result = create_day(CreateDay(operation_id=operation()['operation_id'], day=FIXTURE))
    print(f'Fictional day: {result.id}')


if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) > 1 else ''
    if os.environ.get('APP_MODE') == 'private-local':
        from .private_storage import migrate as private_migrate, cleanup as private_cleanup
        from .auth import provision
        if action == 'migrate':
            private_migrate()
        elif action == 'cleanup':
            private_cleanup()
        elif action == 'provision' and len(sys.argv) == 3:
            if sys.argv[2].strip().casefold().startswith('synthetic-'):
                raise SystemExit('Navneområdet synthetic- er reservert for engangstester.')
            # No password flags, environment variables or fallback echoing input.
            import warnings
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('error', getpass.GetPassWarning)
                    password = getpass.getpass('Passord (minst 12 tegn): ')
                    confirm = getpass.getpass('Gjenta passord: ')
            except getpass.GetPassWarning:
                raise SystemExit('Skjult passordinntasting krever en terminal.') from None
            if password != confirm:
                raise SystemExit('Passordene er ikke like.')
            try:
                provision(sys.argv[2], password)
            except Exception:
                raise SystemExit('Kunne ikke opprette konto. Kontroller brukernavn og passordkrav.') from None
            print('Konto opprettet.')
        else:
            raise SystemExit('Private mode: migrate | cleanup | provision USERNAME')
    elif action == 'migrate':
        migrate()
    elif action == 'cleanup':
        cleanup()
    elif action == 'seed':
        with database() as conn:
            exists = conn.execute('SELECT id FROM fictional_days WHERE expires_at > clock_timestamp() LIMIT 1').fetchone()
        if exists:
            print(f'Fictional day already present: {exists["id"]}')
        else:
            seed()
    elif action == 'reset' and sys.argv[2:] == ['--fictional-only']:
        with database() as conn:
            conn.execute('TRUNCATE fictional_days, creation_operations')
        seed()
    else:
        raise SystemExit('Use migrate | seed | cleanup | reset --fictional-only')
