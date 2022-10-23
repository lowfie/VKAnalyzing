from loader import Base, engine
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, BigInteger, Text, Boolean, DateTime, ForeignKey


class Group(Base):
    __tablename__ = "groups"

    group_id = Column("group_id", Integer, primary_key=True)
    group_name = Column("group_name", Text)
    screen_name = Column("screen_name", Text)
    group_members = Column("members", Integer, default=0)
    autoparse = Column("is_autoparse", Boolean, default=False)
    post = relationship("Post", lazy="select")

    def __repr__(self):
        return f"<Group id={self.id} group_name={self.group_name}>"


class Post(Base):
    __tablename__ = "posts"

    post_id = Column("post_id", Integer, primary_key=True)
    owner_id = Column("owner_id", Integer)
    group_id = Column(Integer, ForeignKey(Group.group_id), nullable=False)
    likes = Column("likes", Integer, default=0)
    quantity_comments = Column("quantity_comments", Integer, default=0)
    reposts = Column("reposts", Integer, default=0)
    views = Column("views", BigInteger, default=0)
    photo = Column("is_photo", Boolean)
    post_text = Column("text", Text)
    positive_comments = Column("positive_comments", Integer, default=0)
    negative_comments = Column("negative_comments", Integer, default=0)
    date = Column("date", DateTime)
    comment = relationship("Comment", lazy="select")

    def __repr__(self):
        return f"<Post post_id={self.post_id} post_text={self.post_text[:20]}>"


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column("comment_id", Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.post_id), nullable=False)
    text = Column("text", Text)
    tone = Column("tone", Text)

    def __repr__(self):
        return f"<Comment comment_id={self.comment_id} comment_text={self.group_name}>"


def create_tables() -> None:
    """Автоматическое создание моделей при запуске"""
    Base.metadata.create_all(bind=engine)
