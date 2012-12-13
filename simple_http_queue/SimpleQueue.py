import sqlite3
import os
try:
    from thread import get_ident
except ImportError:
    from dummy_thread import get_ident

#
# Code largely inspired by Thiago Arruda: http://flask.pocoo.org/snippets/88/
#

class SimpleQueue(object):
    createSql = 'CREATE TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)'
    dropSql = "DROP TABLE IF EXISTS %s"
    sizeSql = 'SELECT COUNT(*) FROM %s'
    peekSql = 'SELECT id, data FROM %s ORDER BY id DESC LIMIT 1'
    pushSql = 'INSERT INTO %s (data) VALUES(?)'
    popSql = 'DELETE FROM %s WHERE id=%d'
    writeLockSql = 'BEGIN IMMEDIATE'

    def __init__(self, path, name):
	self.path = os.path.abspath(path)
	self._connection_cache = {}
	self.name = name
        with self._get_conn() as conn:
            conn.execute(self.createSql%name)

    def _get_conn(self):
        id = get_ident()
        if id not in self._connection_cache:
            self._connection_cache[id] = sqlite3.Connection(self.path, 
                    timeout=60)
        return self._connection_cache[id]

    def pop(self):
	with self._get_conn() as conn:
	    conn.execute(self.writeLockSql)
            cursor = conn.execute(self.peekSql%self.name)
	    try:
	        id, obj_buffer = cursor.next()
            except StopIteration:
                conn.commit() # unlock the database
		return None
	
	    if id:
                conn.execute(self.popSql%(self.name, id))
                return str(obj_buffer)
	    return None

    def peek(self):
	with self._get_conn() as conn:
            cursor = conn.execute(self.peekSql%self.name)
            try:
                return str(cursor.next()[0])
            except StopIteration:
                return None
	return None

    def size(self):
	with self._get_conn() as conn:
            cursor = conn.execute(self.sizeSql%self.name)
            try:
                return str(cursor.next()[0])
            except StopIteration:
                return None
	return None

    def push(self, data):
        with self._get_conn() as conn:
            try:
            	conn.execute(self.pushSql%self.name, (buffer(data),)) 
            except StopIteration:
		return False
	return True

    def drop(self):
        with self._get_conn() as conn:
            conn.execute(self.dropSql%self.name) 
	
