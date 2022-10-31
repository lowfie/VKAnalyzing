from loguru import logger
from sqlalchemy import inspect

from app.database.models import Post, Comment, Group
from app.loader import engine, Base


def table_exist(table_name: str) -> bool:
    return inspect(engine).has_table(table_name)


def create_tables_if_not_exist() -> None:
    """Автоматическое создание моделей при запуске"""
    models = [Post, Comment, Group]
    existing_tables = [table_exist(name.__tablename__) for name in models]
    if not all(existing_tables):
        Base.metadata.create_all(bind=engine)
        logger.info("Таблицы созданы, так как их не было в базе данных!")
