import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = 'logs/app.log'
    MAX_TASKS_PER_USER = 50
    JWT_EXPIRATION_DELTA = timedelta(hours=24)
    TASK_PRIORITY_LEVELS = {
        1: 'Низкий',
        2: 'Средний',
        3: 'Высокий',
        4: 'Срочный',
        5: 'Критический'
    }
