import datetime
import sqlalchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(UserMixin, SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    # is_active = sqlalchemy.Column(sqlalchemy.Boolean,
    #                                  default=True)
    # is_authenticated = sqlalchemy.Column(sqlalchemy.Boolean,
    #                               default=False)
    # categories = orm.relation("Categories", back_populates='user')

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)


    # def get_id(self):
    #     return self.id
