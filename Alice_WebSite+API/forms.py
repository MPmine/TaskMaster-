from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateTimeField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from models import User
from wtforms.validators import ValidationError
from config import Config  # предполагаем, что Config импортируется отсюда


class TaskForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(message='Название задачи обязательно'),
            Length(max=100, message='Название не должно превышать 100 символов')
        ]
    )
    description = TextAreaField('Description')
    status = SelectField(
        'Status',
        choices=[
            ('pending', 'Ожидает'),
            ('in_progress', 'В работе'),
            ('completed', 'Завершена'),
            ('cancelled', 'Отменена')
        ],
        default='pending'
    )
    priority = SelectField(
        'Priority',
        choices=[(str(i), Config.TASK_PRIORITY_LEVELS[i]) for i in range(1, 6)],
        coerce=int
    )
    due_date = DateTimeField(
        'Due Date (YYYY-MM-DD HH:MM)',
        format='%Y-%m-%d %H:%M'
        # Поле необязательно — просто не добавляем DataRequired()
    )
    submit = SubmitField('Save Task')



class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Имя пользователя обязательно'),
            Length(min=3, max=80, message='Имя должно быть от 3 до 80 символов')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email обязателен'),
            Email(message='Введите корректный email')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Пароль обязателен'),
            Length(min=6, message='Пароль должен быть не менее 6 символов')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Подтвердите пароль'),
            EqualTo('password', message='Пароли должны совпадать')
        ]
    )
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Пользователь с таким email уже существует')



class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(message='Имя пользователя обязательно')]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Пароль обязателен')]
    )
    submit = SubmitField('Login')
