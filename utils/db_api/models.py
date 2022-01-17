from sqlalchemy import Column, BIGINT, Integer, String, ForeignKey, orm, Date, Time
from sqlalchemy.orm import relation, relationship

from utils.db_api.database import base


class Users(base):
    __tablename__ = 'users'
    chat_id = Column(Integer, primary_key=True)
    full_name = Column(String)

    groups_id = relationship("Groups", cascade="all, delete")
    groups = relation("Groups", primaryjoin="Users.chat_id == Groups.user_id")

    def __repr__(self):
        return f'{self.chat_id}:{self.full_name}'


class Groups(base):
    __tablename__ = 'groups'
    chat_id = Column(BIGINT, primary_key=True)
    user_id = Column(ForeignKey("users.chat_id"))
    name = Column(String)

    links = orm.relation("Links", primaryjoin="Groups.chat_id == Links.groups_id")

    def __repr__(self):
        return f'{self.chat_id}:{self.name}'


class Links(base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True, autoincrement=True)
    groups_id = Column(ForeignKey("groups.chat_id"))
    name = Column(String)
    url = Column(String)

    def __repr__(self):
        return f'{self.name}:{self.groups_id}'


class DateTimeForLinks(base):
    __tablename__ = 'datetime_for_link'
    id = Column(Integer, primary_key=True, autoincrement=True)
    links_id = Column(ForeignKey("links.id"))
    date = Column(Date)
    time = Column(Time)

    def __repr__(self):
        return f'{self.links_id}:{self.date}:{self.time}'
