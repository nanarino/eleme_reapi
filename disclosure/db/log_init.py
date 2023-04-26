import sqlite3
import pathlib

def log_init():
  with open(pathlib.Path('./log_init.sql')) as sql:
    conn = sqlite3.connect(pathlib.Path('./log.db'))
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()