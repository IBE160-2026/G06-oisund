import os
import uvicorn

if __name__ == '__main__':
    if os.environ.get('APP_MODE') == 'private-local':
        from .auth import configuration
        from .private_storage import migrate
        configuration()
        target = 'app.private_main:app'
    else:
        from .storage import migrate
        target = 'app.main:app'
    migrate()
    uvicorn.run(target, host='0.0.0.0', port=8000, access_log=False, proxy_headers=False)
