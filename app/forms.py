from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField,
                     IntegerField, BooleanField, PasswordField, EmailField, DecimalField)
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    name = StringField("Имя: ", validators=[DataRequired()])
    email = EmailField("Email: ", validators=[Email()])
    login = StringField('Логин:', validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired(), Length(min=4, max=100)])
    age = IntegerField("Возвраст: ", validators=[DataRequired()])
    submit = SubmitField("Регистрация")

class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль:", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Запомнить")
    submit = SubmitField('Войти')

class GameForm(FlaskForm):
    title = StringField("Название: ", validators=[DataRequired()])
    description = TextAreaField("Описание: ", validators=[DataRequired()])
    cost = DecimalField('Цена:', validators=[DataRequired()])
    size = DecimalField("Вес Gb:", validators=[DataRequired()])
    age_limited = BooleanField("18+")
    submit = SubmitField("Добавить игру")