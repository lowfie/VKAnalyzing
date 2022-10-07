from loader import session

from loguru import logger


class GroupService:

    def __init__(self, group):
        self.group = group

    def add(self, input_data: dict):
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
            logger.error(f'Произошла ошибка при сохранении Поста, Текст ошибки:\n{err}')
            session.rollback()

    def update(self, input_data: dict):
        """
        Функция принимает словарь с данными
        и обновляет их
        """
        group = session.query(self.group).filter(self.group.group_id == input_data['group_id']).first()
        if not group:
            raise ValueError('Такого поста нет в бд')
        group.group_name = input_data['name']
        group.screen_name = input_data['screen_name']
        group.group_members = input_data['members']
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении Поста, Текст ошибки:\n{err}')
            session.rollback()


class PostService:

    def __init__(self, post):
        self.post = post

    def add(self, input_data: dict):
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
            logger.error(f'Произошла ошибка при сохранении Поста, Текст ошибки:\n{err}')
            session.rollback()

    def update(self, input_data: dict):
        """
        Функция принимает словарь с данными
        и обновляет их
        """
        post = session.query(self.post).filter(self.post.post_id == input_data['post_id']).first()
        if not post:
            raise ValueError('Такого поста нет в бд')
        post.quantity_comments = input_data['quantity_comments']
        post.likes = input_data['likes']
        post.views = input_data['views']
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении Поста, Текст ошибки:\n{err}')
            session.rollback()

    def update_tonal_comments(self, tone, where_post):
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
            logger.error(f'Произошла ошибка при сохранении Поста, Текст ошибки:\n{err}')
            session.rollback()


class CommentService:

    def __init__(self, comment):
        self.comment = comment

    def add(self, input_data: dict):
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
            logger.error(f'Произошла ошибка при сохранении Поста, Текст ошибки:\n{err}')
            session.rollback()

    def update(self, input_data: dict):
        """
        Функция принимает на вход метаданные комментария
        и обновляет их
        """
        comment = session.query(self.comment).filter(self.comment.comment_id == input_data['comment_id']).first()
        if not comment:
            raise ValueError('Такого комментария нет в бд')
        comment.text = input_data['text']
        try:
            session.commit()
        except Exception as err:
            logger.error(f'Произошла ошибка при сохранении Поста, Текст ошибки:\n{err}')
            session.rollback()
