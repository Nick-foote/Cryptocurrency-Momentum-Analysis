from contextlib import contextmanager
from psycopg2 import sql

# --- PostGreSQL Queries ---

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS {asset} (
        Fast_EMA INTEGER,
        Slow_EMA INTEGER,
        ROI_percent INTEGER,
        UNIQUE (Fast_EMA, Slow_EMA)
    );"""


# -- Functions --

def create_table(user_asset: str):
    CREATE_PROFIT_COMPARISON_TABLE = sql.SQL(CREATE_TABLE)
    table_query = CREATE_PROFIT_COMPARISON_TABLE.format(asset=sql.Identifier(user_asset))
    return table_query


def insert_values(user_asset: str):
    INSERT_EMA_VALUES = sql.SQL("INSERT INTO {asset} VALUES (%s, %s, %s);")
    insert_query = INSERT_EMA_VALUES.format(asset=sql.Identifier(user_asset))
    return insert_query


def select_best_20(user_asset: str):
    SELECT_20_BEST_RESULTS = sql.SQL("SELECT * FROM {asset} ORDER BY roi_percent DESC LIMIT 20;")
    select_query = SELECT_20_BEST_RESULTS.format(asset=sql.Identifier(user_asset))
    return select_query




@contextmanager
def get_cursor(connection):
    """passing through connection from app taken from connection_pool,
    and turning it into a cursor"""
    with connection:
        with connection.cursor() as cursor:
            yield cursor

# -- SQL Queries --


def create_ema_table(connection, user_asset: str):
    table_query = create_table(user_asset)

    with get_cursor(connection) as cursor:
        cursor.execute(table_query)


def insert_ema_values(connection, user_asset: str, ema_fast: int, ema_slow: int, ROI_percent: int):
    insert_query = insert_values(user_asset)

    with get_cursor(connection) as cursor:
        cursor.execute(insert_query, (ema_fast, ema_slow, ROI_percent))


def get_top_20_results(connection, user_asset: str):
    select_query = select_best_20(user_asset)

    with get_cursor(connection) as cursor:
        cursor.execute(select_query)
        return cursor.fetchall()
