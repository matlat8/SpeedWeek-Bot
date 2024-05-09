import glob
import os

from db import DB

db = DB(1, 10)

def setup_database():
    conn = db.get_conn()
    cursor = conn.cursor()

    for filename in glob.glob('setup/sql/t_*.sql'):
        with open(filename, 'r') as f:
            cursor.execute(f.read())

    conn.commit()
    db.release_conn(conn)

