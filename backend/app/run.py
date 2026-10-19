import uvicorn
from .storage import migrate

if __name__ == '__main__':
    migrate()
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000)
