from loader import session

from loguru import logger

from typing import Any
from loader import Base


class GroupService:

    def __init__(self, group: Base) -> None:
        self.group = group
        print(type(self.group))

    def add(self, input_data: dict[str, Any]) -> None:
        """
        Функция принимает словарь с данными группы
        и добавляет эти данные бд, если их не существует
        """
        new_group = self.group(
            group_id=input_data['group_id'],
            group_name=input_data['name'],
            screen_name=input_data['screen_name'],
            group_members=input_data['members']
        )
        session.add(new_group)
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении группы: {err}')
            session.rollback()

    def update(self, input_data: dict[str, Any]) -> None:
        """
        Функция принимает словарь с данными
        и обновляет их
        """
        group = session.query(self.group).filter(self.group.group_id == input_data['group_id']).first()
        if not group:
            logger.warning(f'Такой группы нет в бд: {group}')
            raise ValueError('Такой группы нет в бд')
        group.group_name = input_data['name']
        group.screen_name = input_data['screen_name']
        group.group_members = input_data['members']
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при обновлении группы: {err}')
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


class PostService:

    def __init__(self, post: Base) -> None:
        self.post = post

    def add(self, input_data: dict[str, Any]) -> None:
        """
        Функция принимает словарь с данными поста
        и добавляет эти данные бд, если их не существует
        """
        new_post = self.post(
            post_id=input_data['post_id'],
            owner_id=input_data['owner_id'],
            group_id=input_data['group_id'],
            quantity_comments=input_data['quantity_comments'],
            reposts=input_data['reposts'],
            likes=input_data['likes'],
            views=input_data['views'],
            photo=input_data['photo'],
            post_text=input_data['text'],
            date=input_data['date']
        )
        session.add(new_post)
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении поста: {err}')
            session.rollback()

    def update(self, input_data: dict[str, Any]) -> None:
        """
        Функция принимает словарь с данными
        и обновляет их
        """
        post = session.query(self.post).filter(self.post.post_id == input_data['post_id']).first()
        if not post:
            logger.warning(f'Такого поста нет в бд: {post}')
            raise ValueError('Такого поста нет в бд')
        post.quantity_comments = input_data['quantity_comments']
        post.likes = input_data['likes']
        post.views = input_data['views']
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при обновлении поста: {err}')
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

    def add(self, input_data: dict[str, Any]) -> None:
        """
        Функция принимает словарь метаданных комментария
        И добавляет в бд
        """
        new_comment = self.comment(
            comment_id=input_data['comment_id'],
            post_id=input_data['post_id'],
            text=input_data['text'],
            tone=input_data['tone']
        )
        session.add(new_comment)
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении комментария: {err}')
            session.rollback()

    def update(self, input_data: dict[str, Any]) -> None:
        """
        Функция принимает на вход метаданные комментария
        и обновляет их
        """
        comment = session.query(self.comment).filter(self.comment.comment_id == input_data['comment_id']).first()
        if not comment:
            logger.warning(f'Такого комментария нет в бд {comment}')
            raise ValueError('Такого комментария нет в бд')
        comment.text = input_data['text']
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при обновлении комментария: {err}')
            session.rollback()
