import flask
from data import db_session
from data.__all_models import Jobs, User
from flask import jsonify, make_response, request
from sqlalchemy.exc import IntegrityError


jobs_api_blueprint = flask.Blueprint('jobs_api', __name__)


# noinspection PyUnusedLocal
@jobs_api_blueprint.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@jobs_api_blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify({
        'jobs': [item.to_dict()
                 for item in jobs]
    })


@jobs_api_blueprint.route('/api/jobs/<int:job_id>')
def get_jobs_by_id(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if jobs:
        return jsonify({'job': jobs.to_dict()})
    else:
        return jsonify({'error': 'Not found'})


@jobs_api_blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ('id', 'team_leader_id', 'job', 'work_size',
                                                 'is_finished', 'collaborators')):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    try:
        # noinspection PyArgumentList
        jobs = Jobs(id=request.json['id'],
                    team_leader_id=request.json['team_leader_id'],
                    job=request.json['job'],
                    work_size=request.json['work_size'],
                    is_finished=request.json['is_finished'])
        for user_id in request.json['collaborators']:
            jobs.collaborators.append(session.query(User).filter(User.id == user_id).first())
        session.add(jobs)
        session.commit()
    except IntegrityError:
        return jsonify({'error': 'Id already exists'})
    return jsonify({'success': 'OK'})


@jobs_api_blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_jobs(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    session.delete(jobs)
    session.commit()
    return jsonify({'success': 'OK'})


@jobs_api_blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_jobs(job_id):
    job_fields = ['team_leader_id', 'job', 'work_size', 'is_finished', 'collaborators']
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    if not request.json:
        return jsonify({'error': 'Empty request'})
    if 'id' in request.json or any([key not in job_fields for key in request.json]):
        return jsonify({'error': 'Bad request'})
    for field in job_fields[:-1]:
        if field in request.json:
            jobs.__setattr__(field, request.json[field])
    if 'collaborators' in request.json:
        jobs.collaborators[:] = [session.query(User).get(i) for i in request.json['collaborators']]
    session.commit()
    return jsonify({'success': 'OK'})
