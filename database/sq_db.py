import sqlite3 as sq
import os


def create_api() -> None:
    """Создаёт таблицу 'api' в БД."""
    with sq.connect(os.path.join('database', 'data_base.db')) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS api(
        id_api INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_user_id INTEGER,
        key TEXT,
        secret TEXT
        )""")


async def insert_api(data: dict) -> None:
    """Создать запись в таблице 'api'."""
    with sq.connect(os.path.join('database', 'data_base.db')) as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO api VALUES (NULL, ?, ?, ?)",
            (data['tg_user_id'], data['key'], data['secret']),
        )


async def select_api(tg_user_id: int) -> tuple:
    """Прочитать запись в таблице 'api'."""
    with sq.connect(os.path.join('database', 'data_base.db')) as con:
        cur = con.cursor()
        row_from_api: tuple = cur.execute(
            f"""SELECT tg_user_id, key, secret
            FROM api
            WHERE tg_user_id = {tg_user_id}"""
        ).fetchone()
    return row_from_api


async def update_api(tg_user_id: int, key: str, secret: str) -> None:
    """Обновить key и secret в таблице 'api'."""
    with sq.connect(os.path.join('database', 'data_base.db')) as con:
        cur = con.cursor()
        cur.execute(
            f"""UPDATE api
            SET key = '{key}', secret = '{secret}'
            WHERE tg_user_id = {tg_user_id}"""
        )
