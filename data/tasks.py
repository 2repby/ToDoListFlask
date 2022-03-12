import datetime
import sqlalchemy
from sqlalchemy import orm


from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    deadline = sqlalchemy.Column(sqlalchemy.DateTime,
                                 default=datetime.datetime.now() + datetime.timedelta(days=7))
    done = sqlalchemy.Column(sqlalchemy.Integer)
    category_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("categories.id"))

    category = orm.relation('Category')

