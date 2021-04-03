import sqlalchemy
from .db_session import SqlAlchemyBase
from .users import User
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


jobs_to_collaborators = sqlalchemy.Table('jobs_to_collaborators', SqlAlchemyBase.metadata,
                                         sqlalchemy.Column('jobs', sqlalchemy.Integer,
                                                           sqlalchemy.ForeignKey('jobs.id')),
                                         sqlalchemy.Column('collaborator',
                                                           sqlalchemy.Integer,
                                                           sqlalchemy.ForeignKey('users.id')))


class Jobs (SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'
    serialize_only = ('team_leader', 'collaborators', 'job', 'work_size')
    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True, autoincrement=True)
    team_leader_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    team_leader = orm.relationship(User, foreign_keys=[team_leader_id])
    collaborators = orm.relationship(User, secondary='jobs_to_collaborators', backref="collaborator")
