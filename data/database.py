from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
base = declarative_base()


class User(base):
    __tablename__ = 'users'
    snils = Column(String, primary_key=True)
    user_id = Column(Integer)
    place = Column(Integer)

    def __repr__(self):
        return f'{self.snils}:{self.user_id}:{self.place}'


base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
