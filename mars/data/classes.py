from flask_wtf import FlaskForm
from flask import url_for
from wtforms import PasswordField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    id = IntegerField('id астронавта', validators=[DataRequired()])
    pas = PasswordField('Пароль астронавта', validators=[DataRequired()])
    cap_id = IntegerField('id капитана', validators=[DataRequired()])
    cap_pas = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')


class GalleryForm(FlaskForm):
    image = FileField('Добавить картинку', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Отправить')