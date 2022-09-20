from models import Post, Comment
from loader import session


class Service:

    @staticmethod
    def add_post(post_data):
        """
        Функция принимает словарь с данными поста
        и добавляет эти данные бд, если их не существует
        """
        post = Post(
            post_id=post_data['id'],
            owner_id=post_data['owner_id'],
            group=post_data['group'],
            quantity_comments=post_data['quantity_comments'],
            likes=post_data['likes'],
            views=post_data['views'],
            photo=post_data['photo'],
            post_text=post_data['text']
        )
        session.add(post)
        session.commit()

    @staticmethod
    def update_post(post_data):
        """
        Функция принимает словарь с данными
        и обновляет их
        """
        post = session.query(Post).filter(Post.post_id == post_data['id']).first()
        post.quantity_comments = post_data['quantity_comments']
        post.likes = post_data['likes']
        post.views = post_data['views']
        session.commit()

    @staticmethod
    def add_comment(comment_data):
        """
        Функция принимает словарь метаданных комментария
        И добавляет в бд
        """
        comment = Comment(
            comment_id=comment_data['comment_id'],
            post_id=comment_data['post_id'],
            text=comment_data['text']
        )
        session.add(comment)
        session.commit()

    @staticmethod
    def update_comment(comment_data):
        """
        Функция принимает на вход метаданные комментария
        и обновляет их
        """
        comment = session.query(Comment).filter(Comment.comment_id == comment_data['comment_id']).first()
        comment.text = comment_data['text']
        session.commit()
