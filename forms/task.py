from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    title = StringField('Наименование задачи', validators=[DataRequired(), Length(min=4, max=25)])
    deadline = DateTimeLocalField('Срок выполнения', validators=[DataRequired()])
    category = SelectField("Категория задачи", validate_choice=False, choices=[])
    submit = SubmitField('Добавить')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if kwargs.get('categories', False):
            self.category.choices = list(map(lambda x: (x.id, x.title),kwargs['categories']))
