from flask import send_file
from flask_restful import Resource, reqparse
import uuid
from src.extensions import api_bp

note_put_args = reqparse.RequestParser()
note_put_args.add_argument("creator", type=str, help="person who created the task")
note_put_args.add_argument("note", type=str, help="description of the task")


class Todo(Resource):
    notes = {}

    def post(self):
        print("in todo post")
        args = note_put_args.parse_args()
        new_id = str(uuid.uuid1().hex)
        args["id"] = new_id
        self.notes[new_id] = args
        print(args)
        return args

'''
@api_bp.teardown_request
def teardown(error=None):
    try:
        print("inside todo teardown")
    except:
        print("in except")
'''