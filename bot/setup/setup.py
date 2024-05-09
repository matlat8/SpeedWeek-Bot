

from db import DB

db = DB(1, 10)

def setup_database():
    db.get_conn()

