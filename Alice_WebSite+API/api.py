from flask_restful import Api, Resource, reqparse
from models import User, Task, db
from flask import jsonify
from datetime import datetime

api = Api()

class UserListAPI(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = User(username=args['username'], email=args['email'])
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class TaskListAPI(Resource):
    def get(self, user_id=None):
        if user_id:
            tasks = Task.query.filter_by(user_id=user_id).all()
        else:
            tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str)
        parser.add_argument('status', type=str, default='pending')
        parser.add_argument('priority', type=int, default=1)
        parser.add_argument('due_date', type=lambda x: datetime.fromisoformat(x) if x else None)
        parser.add_argument('user_id', type=int, required=True)
        args = parser.parse_args()

        task = Task(**args)
        db.session.add(task)
        db.session.commit()
        return task.to_dict(), 201

class TaskAPI(Resource):
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return task.to_dict()

    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('status', type=str)
        parser.add_argument('priority', type=int)
        parser.add_argument('due_date', type=lambda x: datetime.fromisoformat(x) if x else None)
        args = parser.parse_args()

        for key, value in args.items():
            if value is not None:
                setattr(task, key, value)
        db.session.commit()
        return task.to_dict()

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {'message': 'Task deleted'}, 204

# Регистрация ресурсов API
api.add_resource(UserListAPI, '/api/users', '/api/users/')
api.add_resource(TaskListAPI, '/api/tasks', '/api/users/<int:user_id>/tasks')
api.add_resource(TaskAPI, '/api/tasks/<int:task_id>')
