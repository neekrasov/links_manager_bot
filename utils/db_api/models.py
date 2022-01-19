from sqlalchemy import Column, BIGINT, Integer, String, ForeignKey, orm, Date, Time, Boolean
from sqlalchemy.orm import relation

from utils.db_api.database import db


class User(db.Model):
    __tablename__ = 'user'
    chat_id = Column(Integer, primary_key=True)
    full_name = Column(String)

    def __repr__(self):
        return f'{self.chat_id}:{self.full_name}'


class Group(db.Model):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BIGINT)
    name = Column(String)
    admin_id = Column(ForeignKey("user.chat_id"))

    def __repr__(self):
        return f'{self.chat_id}:{self.name}'


class GroupUsers(db.Model):
    __tablename__ = 'group_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(ForeignKey("group.id"))
    user_id = Column(ForeignKey("user.chat_id"))

    users = orm.relation("User", primaryjoin="GroupUsers.user_id == User.chat_id")

    def __repr__(self):
        return f'{self.group_id}:{self.user_id}'


class Link(db.Model):
    __tablename__ = 'link'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(ForeignKey("group.id"))
    name = Column(String)
    url = Column(String)
    one_time = Column(Boolean)

    def __repr__(self):
        return f'{self.name}:{self.groups_id}'


class DateTimeForLink(db.Model):
    __tablename__ = 'datetime_for_link'
    id = Column(Integer, primary_key=True, autoincrement=True)
    links_id = Column(ForeignKey("link.id"))
    date = Column(Date)
    time_start = Column(Time)
    time_end = Column(Time)
    repeat = Column(Time)

    link = orm.relation('Link')

    def __repr__(self):
        return f'{self.links_id}:{self.date}:{self.time}'
