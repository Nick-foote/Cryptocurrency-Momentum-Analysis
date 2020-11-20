import os
from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

# Set up the PostGreSQL connection, keeping my personal URL hidden
load_dotenv()
database_uri = os.environ["DATABASE_URI"]


#  -- Connections Setup --

# Sets up a connection pool for transacions to get and put back.
# This means we don't have to create a new transaction for every PostGreSQL query
pool = SimpleConnectionPool(minconn=1, maxconn=5, dsn=database_uri)


# allows a connection using a 'with statement'.
# yield connection to return results. And when done puts the connection back in the pool
@contextmanager
def get_connection():
    connection = pool.getconn()
    try:
        yield connection
    finally:
        pool.putconn(connection)