from typing import Any
from loguru import logger
from sqlalchemy import inspect
from exceptions import DBSaveError
from loader import session, engine, Base
from database.models import Group, Post, Comment


class GroupService:
    def __init__(self, group: Base) -> None:
        self.group = group

    def add_all(self, input_data: list[dict[str, Any]]) -> None:
        """
        Функция принимает список словарей с данными групп
        и добавляет эти данные бд
        """
        session.bulk_insert_mappings(self.group, input_data)
        try:
            session.commit()
        except DBSaveError as err:
            logger.error(f"Произошла ошибка при сохранении группы: {err}")
            session.rollback()

    def update_all(self, input_data: list[dict[str, Any]]) -> None:
        """
        Функция принимает список словарей с данными групп
        и обновляет их в бд
        """
        session.bulk_update_mappings(self.group, input_data)
        try:
            session.commit()
        except DBSaveError as err:
            logger.error(f"Произошла ошибка при сохранении группы: {err}")
            session.rollback()

    def get_group_id(self, screen_name: str) -> int | None:
        """
        Функция принимает название группы и отдаёт её ID
        """
        group_id = (
            session.query(self.group.group_id)
            .filter(self.group.screen_name == screen_name)
            .first()
        )
        group_id = group_id[0] if group_id else group_id
        return group_id

    def set_autoparsing_group(self, group_name: str) -> bool | None:
        """
        Группа принимает на вход название группы,
        ищет её ID в таблице с группами и меняет
        значение в колонке autoparse
        """
        group_id = self.get_group_id(group_name)
        if group_id:
            autoparse_status = (
                not session.query(self.group.autoparse)
                .filter(self.group.group_id == group_id)
                .first()[0]
            )

            column = {"autoparse": autoparse_status}

            session.query(self.group).filter(
                self.group.group_id == self.get_group_id(group_name)
            ).update(column)

            try:
                session.commit()
            except DBSaveError as err:
                logger.error(
                    f"Произошла ошибка при обновлении статуса авто-парсинга: {err}"
                )
                session.rollback()
            return autoparse_status
        return None


class PostService:
    def __init__(self, post: Base) -> None:
        self.post = post

    def add_all(self, input_data: list[dict[str, Any]]) -> None:
        """
        Функция принимает список словарей с данными постов
        и добавляет эти данные бд
        """
        session.bulk_insert_mappings(self.post, input_data)
        try:
            session.commit()
        except DBSaveError as err:
            logger.error(f"Произошла ошибка при сохранении группы: {err}")
            session.rollback()

    def update_all(self, input_data: list[dict[str, Any]]) -> None:
        """
        Функция принимает список словарей с данными постов
        и обновляет их в бд
        """
        session.bulk_update_mappings(self.post, input_data)
        try:
            session.commit()
        except DBSaveError as err:
            logger.error(f"Произошла ошибка при сохранении группы: {err}")
            session.rollback()

    def update_tonal_comments(self, tones_post: dict[str, int]) -> None:
        """
        Функция принимает тон комментария и ID поста
        и обновляет эти параметры в бд
        """
        positive_comment = {
            "positive_comments": (
                self.post.positive_comments + tones_post["positive_comments"]
            )
        }
        negative_comment = {
            "negative_comments": (
                self.post.negative_comments + tones_post["negative_comments"]
            )
        }
        tones = [positive_comment, negative_comment]

        for tone in tones:
            session.query(self.post).filter(
                self.post.post_id == tones_post["post_id"]
            ).update(tone)
        try:
            session.commit()
        except DBSaveError as err:
            logger.error(f"Произошла ошибка при обновлении тональности: {err}")
            session.rollback()


class CommentService:
    def __init__(self, comment: Base) -> None:
        self.comment = comment

    def add_all(self, input_data: list[dict[str, Any]]) -> None:
        """
        Функция принимает список словарей с данными комментариев
        и добавляет эти данные бд
        """
        session.bulk_insert_mappings(self.comment, input_data)
        try:
            session.commit()
        except DBSaveError as err:
            logger.error(f"Произошла ошибка при сохранении группы: {err}")
            session.rollback()

    def update_all(self, input_data: list[dict[str, Any]]) -> None:
        """
        Функция принимает список словарей с данными комментариев
        и обновляет их в бд
        """
        session.bulk_update_mappings(self.comment, input_data)
        try:
            session.commit()
        except DBSaveError as err:
            logger.error(f"Произошла ошибка при сохранении группы: {err}")
            session.rollback()


def table_exist(table_name: str) -> bool:
    return inspect(engine).has_table(table_name)


def create_tables_if_not_exist() -> None:
    """Автоматическое создание моделей при запуске"""
    models = [Post, Comment, Group]
    existing_tables = [table_exist(name.__tablename__) for name in models]
    if not all(existing_tables):
        Base.metadata.create_all(bind=engine)
        logger.info("Таблицы созданы, так как их не было в базе данных!")