"""Local audit hook inherited by spawned PDF processes. Never logs arguments."""
import json
import os
import sys
import _thread

path=os.environ.get('O6_PYTHON_LOG')


def emit(event,name=''):
    if path:
        # Separate files avoid Windows bind-mount append races between processes
        # and threads. One raw write per event; never record SQL or credentials.
        target=path+'.'+str(os.getpid())+'.'+str(_thread.get_ident())
        fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600)
        try:os.write(fd,(json.dumps(dict(event=event,name=name,pid=os.getpid()))+'\n').encode())
        finally:os.close(fd)


def audit(event,args):
    if event=='import':emit(event,str(args[0]))
    elif event in ('ctypes.dlsym','ctypes.dlsym/handle'):emit(event,str(args[1]))
    elif event=='ctypes.dlopen':emit(event,str(args[0]))
    elif event.startswith('sqlite3.'):
        emit(event)
        if os.environ.get('O6_FORBID_SQLITE')=='1':raise RuntimeError('Unexpected SQLite in scoped application path')
    elif event in ('subprocess.Popen','os.posix_spawn','os.exec','os.system'):
        emit(event,os.path.basename(str(args[0])))


sys.addaudithook(audit)
emit('audit_ready')
