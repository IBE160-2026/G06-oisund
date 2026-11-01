"""Harmless positive controls, no exploit input or privileged file operations."""
import ctypes
import json
from pathlib import Path
import sqlite3

db=sqlite3.connect(':memory:')
assert db.execute("SELECT sqlite_compileoption_used('ENABLE_FTS5')").fetchone()[0]==1
db.execute("CREATE VIRTUAL TABLE normal_fts USING fts5(value, detail=none)")
db.execute("INSERT INTO normal_fts(rowid,value) VALUES(1,'hello world')")
assert db.execute("SELECT rowid FROM normal_fts WHERE normal_fts MATCH 'hel*'").fetchall()==[(1,)]
db.close()
acl=ctypes.CDLL('libacl.so.1',use_errno=True)
acl.acl_from_text.argtypes=[ctypes.c_char_p];acl.acl_from_text.restype=ctypes.c_void_p
acl.acl_get_file.argtypes=[ctypes.c_char_p,ctypes.c_int];acl.acl_get_file.restype=ctypes.c_void_p
acl.acl_set_file.argtypes=[ctypes.c_char_p,ctypes.c_int,ctypes.c_void_p];acl.acl_set_file.restype=ctypes.c_int
acl.acl_extended_file.argtypes=[ctypes.c_char_p];acl.acl_extended_file.restype=ctypes.c_int
acl.acl_delete_def_file.argtypes=[ctypes.c_char_p];acl.acl_delete_def_file.restype=ctypes.c_int
acl.acl_free.argtypes=[ctypes.c_void_p]
path=Path('/tmp/o6-owned-file');path.write_text('synthetic');directory=Path('/tmp/o6-owned-directory');directory.mkdir()
value=acl.acl_from_text(b'u::rw-,g::---,o::---');assert value
results={}
try:
    results['set']=acl.acl_set_file(bytes(path),0x8000,value)
    read=acl.acl_get_file(bytes(path),0x8000)
    results['get_nonnull']=bool(read)
    if read:acl.acl_free(read)
    results['extended']=acl.acl_extended_file(bytes(path))
    results['delete_default']=acl.acl_delete_def_file(bytes(directory))
finally:acl.acl_free(value)
print(json.dumps(dict(sqlite_version=sqlite3.sqlite_version,normal_fts5_prefix_query=True,acl_calls=results,
                     synthetic_tmpfs_only=True,negative_rowids_or_symlink_exploit_used=False)))
