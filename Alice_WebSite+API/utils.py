import logging
import json
from datetime import datetime, timedelta
from random import randint, choice
from models import User, Task, db
from config import Config


def setup_logging():
    """
    Настраивает систему логирования приложения.

    Создаёт два обработчика:
    - FileHandler: записывает логи в файл logs/app.log
    - StreamHandler: выводит логи в консоль

    Возвращает настроенный логгер.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)



def calculate_task_analytics(tasks):
    """
    Рассчитывает аналитику по задачам пользователя.

    Параметры:
        tasks (list): список объектов задач

    Возвращает:
        dict: словарь с метриками:
            - total: общее количество задач
            - completed: количество выполненных задач
            - overdue: количество просроченных задач
            - completion_rate: процент выполненных задач
            - overdue_rate: процент просроченных задач
    """
    total = len(tasks)
    completed = len([t for t in tasks if t.status == 'completed'])
    overdue = len([t for t in tasks if t.is_overdue()])

    if total > 0:
        completion_rate = (completed / total) * 100
        overdue_rate = (overdue / total) * 100
    else:
        completion_rate = 0
        overdue_rate = 0

    return {
        'total': total,
        'completed': completed,
        'overdue': overdue,
        'completion_rate': round(completion_rate, 1),
        'overdue_rate': round(overdue_rate, 1)
    }



def generate_sample_data():
    """
    Генерирует тестовые данные для демонстрации работы системы.

    Создаёт 3 пользователей и по 3–8 задач для каждого.
    Используется для начальной настройки или демонстрации.
    """
    logger = setup_logging()

    users_data = [
        {'username': 'alice', 'email': 'alice@example.com'},
        {'username': 'bob', 'email': 'bob@example.com'},
        {'username': 'charlie', 'email': 'charlie@example.com'}
    ]

    task_titles = [
        'Fix critical bug',
        'Write documentation',
        'Review code',
        'Plan next sprint',
        'Test new feature',
        'Update dependencies',
        'Optimize performance'
    ]

    status_options = ['pending', 'in_progress', 'completed']
    priority_options = list(range(1, 6))  # 1–5

    try:
        for user_info in users_data:
            # Проверяем, существует ли пользователь
            existing_user = User.query.filter_by(username=user_info['username']).first()
            if existing_user:
                logger.info(f"User {user_info['username']} already exists, skipping.")
                continue

            user = User(
                username=user_info['username'],
                email=user_info['email']
            )
            user.set_password('password123')  # Стандартный пароль для тестовых пользователей
            db.session.add(user)
            db.session.commit()
            logger.info(f"Created user: {user.username}")

            # Создаём случайные задачи для пользователя
            num_tasks = randint(3, 8)
            for _ in range(num_tasks):
                task = Task(
                    title=choice(task_titles),
                    description=f"Sample task description for {user.username}",
                    status=choice(status_options),
                    priority=choice(priority_options),
            due_date=datetime.utcnow() + timedelta(days=randint(1, 30)),
            user_id=user.id
        )
        db.session.add(task)

        db.session.commit()
        logger.info("Sample data generated successfully.")

    except Exception as e:
        logger.error(f"Error generating sample data: {e}")
        db.session.rollback()



def format_datetime_for_display(dt):
    """
    Форматирует объект datetime для удобного отображения в интерфейсе.

    Параметры:
        dt (datetime): объект datetime

    Возвращает:
        str: отформатированная строка в формате 'DD.MM.YYYY HH:MM'
               или 'Не указана', если dt равен None.
    """
    if dt:
        return dt.strftime('%d.%m.%Y %H:%M')
    return 'Не указана'



def get_priority_display(priority_value):
    """
    Возвращает текстовое представление приоритета задачи.

    Использует настройки из конфигурации.

    Параметры:
        priority_value (int): числовое значение приоритета (1–5)

    Возвращает:
        str: текстовое описание приоритета или 'Неизвестно'
    """
    return Config.TASK_PRIORITY_LEVELS.get(priority_value, 'Неизвестно')



def is_user_task_limit_reached(user_id):
    """
    Проверяет, достиг ли пользователь лимита задач.

    Параметры:
        user_id (int): ID пользователя

    Возвращает:
        bool: True, если лимит достигнут, иначе False
    """
    task_count = Task.query.filter_by(user_id=user_id).count()
    return task_count >= Config.MAX_TASKS_PER_USER




def export_tasks_to_json(user_id):
    """
    Экспортирует задачи пользователя в JSON‑формат.

    Может использоваться для резервного копирования или интеграции.

    Параметры:
        user_id (int): ID пользователя
    Возвращает:
        str: JSON‑строка с задачами пользователя
    """
    tasks = Task.query.filter_by(user_id=user_id).all()
    tasks_data = []

    for task in tasks:
        task_dict = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'created_at': task.created_at.isoformat() if task.created_at else None,
            'due_date': task.due_date.isoformat() if task.due_date else None
        }
        tasks_data.append(task_dict)

    return json.dumps(tasks_data, ensure_ascii=False, indent=2)
