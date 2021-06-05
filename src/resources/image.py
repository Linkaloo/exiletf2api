
from flask import send_file
from flask_restful import Resource, abort, reqparse
import werkzeug
from src.utilities.imageProcessor import ImageProcessor

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

        return send_file(dictionary["new_file"], attachment_filename=dictionary["id"] + ".png")