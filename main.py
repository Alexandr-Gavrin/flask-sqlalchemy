from data import db_session
from sqlalchemy import or_
from flask import Flask, render_template, redirect, request
from data import jobs
from data import users
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'


class RegisterForm(FlaskForm):
    email_login = StringField('Login/email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    db_session.global_init("db/mars_explorer.db")
    sessions = db_session.create_session()
    jobs2 = sessions.query(jobs.Jobs)
    return render_template("Journal_works.html", jobs=jobs2)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_2.data:
            return render_template('register.html', form=form, title='Регистрация',
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email_login.data).first():
            return render_template('register.html', form=form, title='Регистрация',
                                   message="Такой пользователь уже есть")
        user = users.User(
            email=form.email_login.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
    return render_template('register.html', form=form, title='Регистрация')


if __name__ == "__main__":
    db_session.global_init('db/mars_explorer.db')
    app.run()
