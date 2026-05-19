from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """Модель пользователя системы"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с задачами (один ко многим)
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Устанавливает пароль, хешируя его"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверяет пароль путём сравнения хешей"""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Возвращает ID пользователя в строковом формате (требуется Flask-Login)"""
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'


    def to_dict(self):
        """Сериализует объект пользователя в словарь для JSON-ответов"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }



class Task(db.Model):
    """Модель задачи системы"""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    priority = db.Column(db.Integer, default=3)  # 1–5, где 1 — высший приоритет
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def is_overdue(self):
        """Проверяет, просрочена ли задача"""
        if not self.duedate:
            return False
        return datetime.utcnow() > self.duedate

    def __repr__(self):
        return f'<Task {self.title} (User: {self.user_id})>'

    def to_dict(self):
        """Сериализует объект задачи в словарь для JSON-ответов"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'due_date': self.duedate.isoformat() if self.duedate else None,
            'user_id': self.user_id
        }
