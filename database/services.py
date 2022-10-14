from loader import session

from loguru import logger

from typing import Any
from loader import Base


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
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении группы: {err}')
            session.rollback()

    def update_all(self, input_data: list[dict[str, Any]]) -> None:
        """
        Функция принимает список словарей с данными групп
        и обновляет их в бд
        """
        session.bulk_update_mappings(self.group, input_data)
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении группы: {err}')
            session.rollback()

    def get_group_id(self, screen_name: str) -> int | None:
        """
        Функция принимает название группы и отдаёт её ID
        """
        group_id = session.query(self.group.group_id).filter(
            self.group.screen_name == screen_name
        ).first()
        group_id = group_id[0] if group_id else group_id
        return group_id

    def set_autoparsing_group(self, group_name: str) -> bool | None:
        """
        Группа принимает на вход название группы,
        ищет её ID в таблице с группами и меняет
        значение в колонке autoparse
        """
        group_id = self.get_group_id(group_name)
        if not group_id:
            return None
        else:
            autoparse_status = not session.query(self.group.autoparse).filter(
                self.group.group_id == group_id).first()[0]
            column = {'autoparse': autoparse_status}

            session.query(self.group).filter(self.group.group_id == self.get_group_id(group_name)).update(column)

            try:
                session.commit()
            except Exception as err:
                logger.error(f'Произошла ошибка при обновлении статуса авто-парсинга: {err}')
                session.rollback()
            return autoparse_status


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
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении группы: {err}')
            session.rollback()

    def update_all(self, input_data: list[dict[str, Any]]) -> None:
        """
        Функция принимает список словарей с данными постов
        и обновляет их в бд
        """
        session.bulk_update_mappings(self.post, input_data)
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении группы: {err}')
            session.rollback()

    def update_tonal_comments(self, tone: str | None, where_post: int) -> None:
        """
        Функция принимает тон комментария и ID поста
        и обновляет эти параметры в бд
        """
        if tone == 'positive':
            column = {'positive_comments': (self.post.positive_comments + 1)}
        elif tone == 'negative':
            column = {'negative_comments': (self.post.negative_comments + 1)}
        else:
            column = {'negative_comments': self.post.negative_comments}

        session.query(self.post).filter(self.post.post_id == where_post).update(column)

        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при обновлении тональности: {err}')
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
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении группы: {err}')
            session.rollback()

    def update_all(self, input_data: list[dict[str, Any]]) -> None:
        """
        Функция принимает список словарей с данными комментариев
        и обновляет их в бд
        """
        session.bulk_update_mappings(self.comment, input_data)
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении группы: {err}')
            session.rollback()
