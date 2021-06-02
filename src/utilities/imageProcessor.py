from PIL import Image
import requests
import os
import uuid


class ImageProcessor:

    def is_file_image(self, image_url, image_file):
        if image_url is not None:
            return False
        elif image_url is None and image_file is not None:
            return True

    def is_valid(self, is_file, image_url, image_file):
        if is_file:
            extension = image_file.filename[image_file.filename.rfind("."):]
            if extension != ".jpeg" and extension != ".jpg" and extension != ".png" and extension != ".gif":
                return False

        elif not is_file:
            req = requests.get(image_url)
            if req.status_code != 200:
                return False
            extension = req.headers["Content-Type"][req.headers["Content-Type"].rfind("/"):].replace("/", ".")

            if extension != ".jpeg" and extension != ".jpg" and extension != ".png" and extension != ".gif":
                return False

        return True


    def process_image(self, args):
        is_file = self.is_file_image(args["image_url"], args["image_file"])
        is_valid = self.is_valid(is_file, args["image_url"], args["image_file"])
        
        if not is_valid:
            return {"error": "Message"}
        
        image_dictionary = {}
        new_id = str(uuid.uuid1().hex)
        modifier = args["modifier"]

        if modifier == "grayScale":
            image_dictionary["new_image_path"] = os.getcwd() + '\\' + self.convert_to_gray_scale(is_file, args, new_id, image_dictionary)
            return image_dictionary

    def convert_to_gray_scale(self, is_file, args, image_id, dict):
        base_image = image_id + "_input"
        new_image = image_id + "_output"
        
        if is_file is False:
            req = requests.get(args["image_url"])
            extension = req.headers["Content-Type"][req.headers["Content-Type"].rfind("/"):].replace("/", ".")
            img_data = req.content
            base_image += extension
            if extension == ".jpg" or extension == ".jpeg":
                new_image += ".png"
            else:
                new_image += extension 
            
            dict["old_image_path"] = os.getcwd() + "\\" + str(os.getenv("IMAGE_FILE_PATH")) + base_image

            with open(dict["old_image_path"], "wb") as handler:
                handler.write(img_data)

            img = Image.open(os.getenv("IMAGE_FILE_PATH") + base_image).convert("LA")
            img.save(os.getenv("IMAGE_FILE_PATH") + new_image)

            return os.getenv("IMAGE_FILE_PATH") + new_image

        else:
            file = args["image_file"]
            extension = file.filename[file.filename.rfind("."):]
            base_image += extension
            if extension == ".jpg" or extension == ".jpeg":
                new_image += ".png"
            else:
                new_image += extension 


            dict["old_image_path"] = os.getcwd() + "\\" + str(os.getenv("IMAGE_FILE_PATH")) + base_image
            file.save(dict["old_image_path"])

            img = Image.open(os.getenv("IMAGE_FILE_PATH") + base_image).convert("LA")
            img.save(os.getenv("IMAGE_FILE_PATH") + new_image)

            return os.getenv("IMAGE_FILE_PATH") + new_image





