import sys
from .storage import cleanup, database, migrate
from .main import create_day, operation
from .domain import CreateDay, FIXTURE


def seed():
    result = create_day(CreateDay(operation_id=operation()['operation_id'], day=FIXTURE))
    print(f'Fictional day: {result.id}')


if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) > 1 else ''
    if action == 'migrate':
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
