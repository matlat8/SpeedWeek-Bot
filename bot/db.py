import psycopg2.pool
import  asyncpg
import os


class DB:
    def __init__(self, minconn, maxconn):
        connection_string = os.environ.get('POSTGRES_URL')
        self.conn_pool = psycopg2.pool.SimpleConnectionPool(
            minconn,
            maxconn,
            dsn=connection_string
        )

    def get_conn(self):
        return self.conn_pool.getconn()

    def release_conn(self, conn):
        self.conn_pool.putconn(conn)

