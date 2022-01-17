from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data.config import DATABASE_URL

engine = create_engine(DATABASE_URL.replace('postgres', 'postgresql'))
base = declarative_base()
from . import models

base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
