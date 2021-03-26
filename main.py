from flask import Flask
from data import db_session
from data.jobs import Jobs
from data.users import User
from flask import render_template
from forms import *
from flask import redirect
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required
import flask_login
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/mission.db")
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    app.run()


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddingJobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs(team_leader_id=form.team_leader_id.data,
                   job=form.job.data, work_size=int(form.work_size.data),
                   is_finished=form.is_finished.data)
        for user_id in list(map(int, form.collaborators_id.split(', '))):
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
