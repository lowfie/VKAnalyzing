from sqlalchemy import Column, Integer, Text, Boolean

from loader import Base, Engine


class Users(Base):
    __tablename__ = 'users'

    post_id = Column('post_id', Integer, primary_key=True)
    owner_id = Column('owner_id', Integer)
    group_name = Column('group_name', Text)
    quantity_comments = Column('quantity_comments', Integer)
    photo = Column('photo', Boolean)
    quantity_like = Column('quantity_like', Integer)


if __name__ == "__main__":
    Base.metadata.create_all(bind=Engine)
