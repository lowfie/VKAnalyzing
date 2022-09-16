from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from data.config import USER_DB, PASSWORD_DB, HOST_PORT, DATABASE

Engine = create_engine(f"postgresql://{USER_DB}:{PASSWORD_DB}@{HOST_PORT}/{DATABASE}")
Session = scoped_session(sessionmaker(bind=Engine))

Base = declarative_base()
Base.query = Session.query_property()
