from loader import session
from sqlalchemy import func


class PostService:

    def __init__(self, post):
        self.post = post

    def add(self, input_data: dict):
        """
        Функция принимает словарь с данными поста
        и добавляет эти данные бд, если их не существует
        """
        new_post = self.post(
            post_id=input_data['id'],
            owner_id=input_data['owner_id'],
            group=input_data['group'],
            quantity_comments=input_data['quantity_comments'],
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
            print('Произошла ошибка при сохранении Поста, Текст ошибки:', err)
            session.rollback()

    def update(self, input_data: dict):
        """
        Функция принимает словарь с данными
        и обновляет их
        """
        post = session.query(self.post).filter(self.post.post_id == input_data['id']).first()
        if not post:
            raise 'Такого поста нет в бд'
        post.quantity_comments = input_data['quantity_comments']
        post.likes = input_data['likes']
        post.views = input_data['views']
        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при обновлении Поста, Текст ошибки:', err)
            session.rollback()

    def select(self, input_data: dict):
        """
        Функция принимает словарь со значениями
        периода времени и группы, этим данным возвращается
        статистика
        """

        # Количество постов за период
        posts = session.query(self.post).filter(
            self.post.group == input_data['name'],
            self.post.date >= input_data['date']
        ).count()

        # Количество постов с фото/видео за период
        post_with_photo = session.query(self.post).filter(
            self.post.group == input_data['name'],
            self.post.date >= input_data['date'],
            self.post.photo == 'true'
        ).count()

        # Количество лайков со всех постов за период
        likes = session.query(func.sum(self.post.likes)).filter(
            self.post.group == input_data['name'],
            self.post.date >= input_data['date'],
        ).scalar()

        # Количество комментариев с постов
        comments = session.query(func.sum(self.post.quantity_comments)).filter(
            self.post.group == input_data['name'],
            self.post.date >= input_data['date'],
        ).scalar()

        output_data = {
            'count_post': posts,
            'posts_with_photo': post_with_photo,
            'likes': likes,
            'comments': comments
        }

        return output_data


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
            text=input_data['text']
        )
        session.add(new_comment)
        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при сохранении Комментария, Текст ошибки:', err)
            session.rollback()

    def update(self, input_data: dict):
        """
        Функция принимает на вход метаданные комментария
        и обновляет их
        """
        comment = session.query(self.comment).filter(self.comment.comment_id == input_data['comment_id']).first()
        if not comment:
            raise 'Такого комментария нет в бд'
        comment.text = input_data['text']
        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при обновлении Комментария, Текст ошибки:', err)
            session.rollback()
