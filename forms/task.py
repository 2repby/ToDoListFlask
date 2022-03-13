from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, DateTimeLocalField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    title = StringField('Наименование задачи', validators=[DataRequired(), Length(min=4, max=25)])
    deadline = DateTimeLocalField('Срок выполнения', validators=[DataRequired()])
    submit = SubmitField('Добавить')