from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = EmailField('Login/email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    nick = StringField('Придумайте ник', validators=[DataRequired()])
    age = IntegerField('Ваш возраст', validators=[DataRequired()])
    submit = SubmitField('Submit')