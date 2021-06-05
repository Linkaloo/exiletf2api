from PIL import Image
import io
import requests
import uuid


class ImageProcessor:

    def is_file_image(self, image_url, image_file):
        if image_url is not None:
            return False
        elif image_url is None and image_file is not None:
            return True

    def is_valid(self, is_file, url_request : requests.Response, image_file):
        if is_file:
            extension = image_file.filename[image_file.filename.rfind("."):]
            if extension != ".jpeg" and extension != ".jpg" and extension != ".png" and extension != ".gif":
                return False

        elif not is_file:
            if url_request.status_code != 200:
                return False
            
            extension = url_request.headers["Content-Type"][url_request.headers["Content-Type"].rfind("/"):].replace("/", ".")

            if extension != ".jpeg" and extension != ".jpg" and extension != ".png" and extension != ".gif":
                return False

        return True


    def process_image(self, args):
        is_file = self.is_file_image(args["image_url"], args["image_file"])
        req : requests.Response = None

        if not is_file: req = requests.get(args["image_url"])
        
        is_valid = self.is_valid(is_file, req, args["image_file"])

        if not is_valid: return {"error": "Message"}
        
        image_dictionary = {}
        image_dictionary["id"] = str(uuid.uuid1().hex)
        modifier = args["modifier"]

        if modifier == "grayScale":
            image_dictionary["new_file"] = self.convert_to_gray_scale(is_file, args["image_file"], req)
            return image_dictionary

    def convert_to_gray_scale(self, is_file, image_file, req):
        file = None
        if is_file:
            file = image_file.read()
        else:
            file = req.content

        bytes = io.BytesIO(file)

        new_bytes = io.BytesIO()
        img = Image.open(bytes).convert("LA")
        img.save(new_bytes, "PNG")
        new_bytes.seek(0)
        img = new_bytes.read()

        new_bytes = io.BytesIO(img)

        return new_bytes





