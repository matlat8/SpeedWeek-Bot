import psycopg2.pool
import os


class DB:
    def __init__(self, minconn, maxconn):
        self.conn_pool = psycopg2.pool.SimpleConnectionPool(
            minconn,
            maxconn,
            database=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=os.environ.get('POSTGRES_HOST'),
            port=os.environ.get('POSTGRES_PORT')
        )

    def get_conn(self):
        return self.conn_pool.getconn()

    def release_conn(self, conn):
        self.conn_pool.putconn(conn)