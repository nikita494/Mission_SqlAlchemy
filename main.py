from flask import Flask
from data import db_session
from data.jobs import Jobs
from data.users import User
from flask import render_template
from forms import *
from flask import redirect
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()


@app.route('/')
@app.route('/index')
def working_journal():
    db_session.global_init("db/mission.db")
    session = db_session.create_session()
    data = session.query(Jobs).all()
    return render_template('working_journal.html', title='Журнал работ', data=data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_session.global_init("db/mission.db")
        session = db_session.create_session()
        user = User(surname=form.surname, name=form.name, age=form.age, email=form.email,
                    position=form.position, speciality=form.speciality, address=form.address)
        user.set_password(form.password)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
