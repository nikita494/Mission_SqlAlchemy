import sqlalchemy
from .db_session import SqlAlchemyBase
from .users import User
from sqlalchemy import orm

departments_to_members = sqlalchemy.Table('departments_to_members', SqlAlchemyBase.metadata,
                                          sqlalchemy.Column('department', sqlalchemy.Integer,
                                                            sqlalchemy.ForeignKey('departments.id')),
                                          sqlalchemy.Column('member', sqlalchemy.Integer,
                                                            sqlalchemy.ForeignKey('users.id')))


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = orm.relationship(User, foreign_keys=[chief_id])
    members = orm.relationship(User, secondary='departments_to_members', backref="member")
