from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    id = IntegerField('id астронавта', validators=[DataRequired()])
    pas = PasswordField('Пароль астронавта', validators=[DataRequired()])
    cap_id = IntegerField('id капитана', validators=[DataRequired()])
    cap_pas = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')