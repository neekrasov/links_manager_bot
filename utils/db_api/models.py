from sqlalchemy import Column, BIGINT, Integer, String, ForeignKey, orm, Date, Time, Boolean
from sqlalchemy.orm import relation, relationship

from utils.db_api.database import base


class Users(base):
    __tablename__ = 'users'
    chat_id = Column(Integer, primary_key=True)
    full_name = Column(String)

    groups = relation(
        "Groups",
        back_populates='admin',
    )

    def __repr__(self):
        return f'{self.chat_id}:{self.full_name}'


class Groups(base):
    __tablename__ = 'groups'
    chat_id = Column(BIGINT, primary_key=True)
    admin_id = Column(ForeignKey("users.chat_id"))
    name = Column(String)

    links = orm.relation(
        "Links",
        back_populates='group',
    )
    admin = orm.relation('Users')

    def __repr__(self):
        return f'{self.chat_id}:{self.name}'


class GroupUsers(base):
    __tablename__ = 'group_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(ForeignKey("groups.chat_id"))
    user_id = Column(ForeignKey("users.chat_id"))

    users = orm.relation("Users", primaryjoin="GroupUsers.user_id == Users.chat_id")

    def __repr__(self):
        return f'{self.group_id}:{self.user_id}'


class Links(base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(ForeignKey("groups.chat_id"))
    name = Column(String)
    url = Column(String)
    one_time = Column(Boolean)

    group = orm.relation('Groups')

    def __repr__(self):
        return f'{self.name}:{self.groups_id}'


class DateTimeForLinks(base):
    __tablename__ = 'datetime_for_link'
    id = Column(Integer, primary_key=True, autoincrement=True)
    links_id = Column(ForeignKey("links.id"))
    date = Column(Date)
    time_start = Column(Time)
    time_end = Column(Time)
    repeat = Column(Time)

    link = orm.relation('Links')

    def __repr__(self):
        return f'{self.links_id}:{self.date}:{self.time}'
