import os
from flask import send_file, g, jsonify
from flask_restful import Resource, abort, reqparse
import werkzeug
from src.utilities.imageProcessor import ImageProcessor
from src.extensions import api_bp
from src.utilities.schedules import scheduler, file_queue

image_put_args = reqparse.RequestParser()
image_put_args.add_argument("image_url", type=str, help="image url")
image_put_args.add_argument("image_file", type=werkzeug.datastructures.FileStorage, help="image file", location="files", nullable=True)
image_put_args.add_argument("modifier", type=str, help="What to change", required=True)

class Image(Resource):
    image_processor = ImageProcessor()

    def post(self):
        args = image_put_args.parse_args()
        if args["image_url"] is None and args["image_file"] is None:
            abort(400)

        dictionary = self.image_processor.process_image(args)
        if "error" in dictionary:
            abort(400)
        
        g.id = dictionary
        return send_file(dictionary["new_image_path"], as_attachment=True, mimetype="application/octet-stream")

@api_bp.teardown_request
def teardown(error=None):
    try:
        remove_image(g.id)
    except:
        print("Could not add files to queue")
    if error:
        print(error)

def remove_image(image_id):
    if image_id is not None:
        scheduler.pause_job("delete_image_files")
        file_queue.append(image_id["old_image_path"])
        file_queue.append(image_id["new_image_path"])
        scheduler.resume_job("delete_image_files")