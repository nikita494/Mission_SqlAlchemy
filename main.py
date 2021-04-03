from flask import Flask
from data import db_session
from forms import *
from data.__all_models import *
from flask import redirect, request, abort, render_template
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required
from api_jobs import jobs_api_blueprint
import flask_login
app = Flask(__name__, template_folder='templates')
login_manager = LoginManager()


def main():
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.config['JSON_AS_ASCII'] = False
    db_session.global_init("db/mission.db")
    login_manager.init_app(app)
    app.register_blueprint(jobs_api_blueprint)
    app.run()


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddingJobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        # noinspection PyArgumentList
        job = Jobs(team_leader_id=form.team_leader_id.data,
                   job=form.job.data, work_size=int(form.work_size.data),
                   is_finished=form.is_finished.data)
        for user_id in list(map(int, form.collaborators_id.data.split(', '))):
            job.collaborators.append(session.query(User).filter(User.id == user_id).first())
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('adding_job.html', title='Adding a job',
                           current_user=flask_login.current_user, form=form)


@app.route('/')
@app.route('/index')
def working_journal():
    session = db_session.create_session()
    data = session.query(Jobs).all()
    return render_template('working_journal.html', title='Work log',
                           current_user=flask_login.current_user, data=data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        # noinspection PyArgumentList
        user = User(surname=form.surname.data, name=form.name.data, age=form.age.data, email=form.email.data,
                    position=form.position.data, speciality=form.speciality.data, address=form.address.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Registration',
                           current_user=flask_login.current_user, form=form)


@app.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = AddingJobForm()
    if request.method == "GET":
        session = db_session.create_session()
        if flask_login.current_user.id != 1:
            jobs = session.query(Jobs).filter(Jobs.id == job_id,
                                              Jobs.team_leader == flask_login.current_user).first()
        else:
            jobs = session.query(Jobs).filter(Jobs.id == job_id).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.team_leader_id.data = jobs.team_leader_id
            form.is_finished.data = jobs.is_finished
            form.collaborators_id.data = ', '.join([str(i.id) for i in jobs.collaborators])
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        if flask_login.current_user.id != 1:
            jobs = session.query(Jobs).filter(Jobs.id == job_id,
                                              Jobs.team_leader == flask_login.current_user).first()
        else:
            jobs = session.query(Jobs).filter(Jobs.id == job_id).first()
        if jobs:
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.team_leader_id = form.team_leader_id.data
            jobs.is_finished = form.is_finished.data
            for job_id in map(int, form.collaborators_id.data.split(', ')):
                jobs.collaborators.append(session.query(User).filter(User.id == job_id).first())
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('adding_job.html', title='Change Job', form=form,
                           current_user=flask_login.current_user)


@app.route('/delete_job/<int:id>')
@login_required
def delete_job(job_id):
    session = db_session.create_session()
    if flask_login.current_user.id != 1:
        jobs = session.query(Jobs).filter(Jobs.id == job_id,
                                          Jobs.team_leader == flask_login.current_user).first()
    else:
        jobs = session.query(Jobs).filter(Jobs.id == job_id).first()
    if jobs:
        session.delete(jobs)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Authorization',
                               form=form, current_user=flask_login.current_user,
                               message="Неправильный логин или пароль")
    return render_template('login.html', title='Login', form=form, current_user=flask_login.current_user)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
