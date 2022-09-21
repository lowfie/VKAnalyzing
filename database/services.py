from database.models import Post, Comment
from loader import session


class PostService:

    def __init__(self, post):
        self.post = post

    def add(self, input_data: dict):
        """
        Функция принимает словарь с данными поста
        и добавляет эти данные бд, если их не существует
        """
        new_post = Post(
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
        post = session.query(Post).filter(Post.post_id == input_data['id']).first()
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


class CommentService:

    def __init__(self, comment):
        self.comment = comment

    def add(self, input_data: dict):
        """
        Функция принимает словарь метаданных комментария
        И добавляет в бд
        """
        comment = Comment(
            comment_id=input_data['comment_id'],
            post_id=input_data['post_id'],
            text=input_data['text']
        )
        session.add(comment)
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
        comment = session.query(Comment).filter(Comment.comment_id == input_data['comment_id']).first()
        if not comment:
            raise 'Такого комментария нет в бд'
        comment.text = input_data['text']
        try:
            session.commit()
        except Exception as err:
            print('Произошла ошибка при обновлении Комментария, Текст ошибки:', err)
            session.rollback()
