from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask import render_template

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


if __name__ == '__main__':
    main()
