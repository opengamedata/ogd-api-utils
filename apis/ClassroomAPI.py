from flask import Flask
from flask_restful import reqparse, Api, Resource

class ClassroomAPI:
    @staticmethod
    def register(app:Flask):
        api = Api(app)
        api.add_resource(ClassroomAPI.Classroom, '/classroom/<class_id>')
        api.add_resource(ClassroomAPI.Teacher, '/teacher/')
        api.add_resource(ClassroomAPI.Student, '/student/<player_id>')

    class Classroom(Resource):
        def get(self, class_id):
            parser = reqparse.RequestParser()
            parser.add_argument("teacher_id")
            args = parser.parse_args()
            return {
                "classlist":['fake student 1', 'fake student 2', 'fake student 3'],
                "message":f"Found these fake students in fake classroom {class_id}, for fake teacher {args['teacher_id']}"
            }

        def put(self, class_id):
            parser = reqparse.RequestParser()
            parser.add_argument("teacher_id")
            args = parser.parse_args()
            return {
                "message":f"Fake created a fake classroom {class_id} for teacher {args['teacher_id']}"
            }

    class Teacher(Resource):
        def get(self):
            parser = reqparse.RequestParser()
            parser.add_argument("teacher_id")
            return 

    class Student(Resource):
        def get(self, player_id):
            parser = reqparse.RequestParser()
            parser.add_argument("teacher_id")
            args = parser.parse_args()
            return {
                "player":{"name":"fake player", "player_id":player_id},
                "metrics":{"fake metric 1":1, "fake metric 2":"b"},
                "message":f"Got fake player {player_id} for teacher {args['teacher_id']}"
            }
        
        def put(self, player_id):
            parser = reqparse.RequestParser()
            parser.add_argument("teacher_id")
            parser.add_argument("class_id")
            args = parser.parse_args()
            return {
                "message":f"Added fake player {player_id} to fake classroom {args['class_id']} for teacher {args['teacher_id']}"
            }
