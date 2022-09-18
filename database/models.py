from sqlalchemy import Column, Integer, BigInteger, Text, Boolean

from loader import Base, engine


class User(Base):
    __tablename__ = 'users'

    post_id = Column('post_id', Integer, primary_key=True)
    owner_id = Column('owner_id', Integer)
    group = Column('group', Text)
    quantity_comments = Column('quantity_comments', Integer)
    likes = Column('likes', Integer)
    views = Column('views', BigInteger)
    photo = Column('photo', Boolean)
    post_text = Column('text', Text)


class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column('comment_id', Integer, primary_key=True)
    post_id = Column('post_id', Integer)
    comment_text = Column('text', Integer)


def create_db():
    Base.metadata.create_all(bind=engine)
