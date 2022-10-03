from sqlalchemy import Column, Integer, BigInteger, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from loader import Base, engine


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
    date = Column('date', DateTime)
    comment = relationship('Comment', lazy='select')


class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column('comment_id', Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    text = Column('text', Text)
    tone = Column('tone', Text)


def create_tables():
    """Автоматическое создание моделей при запуске"""
    Base.metadata.create_all(bind=engine)
