from os import getenv

from peewee_async import Manager, PostgresqlDatabase

_db = PostgresqlDatabase(
    database=getenv("POSTGRES_DB") or "main",
    user=getenv("POSTGRES_USER") or "postgres",
    host=getenv("POSTGRES_HOST") or "localhost",
    port=getenv("POSTGRES_PORT") or "5432",
    password=getenv("POSTGRES_PASSWORD") or "5573",
)
_db_model_manager = Manager(_db)


def get_db() -> PostgresqlDatabase:
    return _db


def get_db_model_manager() -> Manager:
    return _db_model_manager
