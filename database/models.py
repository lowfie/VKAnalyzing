from sqlalchemy import Column, Integer, BigInteger, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from loader import Base, engine, session


class Post(Base):
    __tablename__ = 'posts'

    post_id = Column('post_id', Integer, primary_key=True)
    owner_id = Column('owner_id', Integer)
    group = Column('group', Text)
    quantity_comments = Column('quantity_comments', Integer)
    likes = Column('likes', Integer)
    views = Column('views', BigInteger)
    photo = Column('photo', Boolean)
    post_text = Column('text', Text)
    comment = relationship('Comment')

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
        post = session.query(Post).first()
        post.quantity_comments = post_data['quantity_comments']
        post.likes = post_data['likes']
        post.views = post_data['views']
        session.commit()


class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column('comment_id', Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    text = Column('text', Text)

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
        comment = session.query(Comment).first()
        comment.text = comment_data['text']
        session.commit()


def create_tables():
    """Автоматическое создание моделей при запуске"""
    Base.metadata.create_all(bind=engine)
