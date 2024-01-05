import os
from typing import Any

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

import base64
import random
import string
import json

app = Flask(__name__, static_url_path="")
CORS(app)

#########################################################################
# Variables
#########################################################################

USER_NAME = "Gill Bates"
USER_EMAIL = "gillbates@macrohard.com"

neuq_global_config = ".neuqconfig"
neuq_global_config_path = os.path.join(os.path.expanduser("~"), neuq_global_config)

neuq_local_folder = ".neuq"
neuq_local_config = "config.json"
neuq_slide_extension = ".slide.json"


#########################################################################
# GLOBAL Config
#########################################################################


# Get username and email from the user
def get_user_info_from_user():
    user_name = input("Enter your name: ")
    user_email = input("Enter your email: ")
    user_data = {"USER_NAME": user_name, "USER_EMAIL": user_email}
    return user_data


# Check if the ".neuqconfig" file exists in users home directory, and if not, create it
if (
    not os.path.exists(neuq_global_config_path)
    or os.path.getsize(neuq_global_config_path) == 0
):
    with open(neuq_global_config_path, "w") as config_file:
        user_data = get_user_info_from_user()
        json.dump(user_data, config_file, indent=4)
        USER_NAME = user_data["USER_NAME"]
        USER_EMAIL = user_data["USER_EMAIL"]
else:
    with open(neuq_global_config_path, "r") as config_file:
        user_data = json.load(config_file)
        try:
            USER_NAME = user_data["USER_NAME"]
            USER_EMAIL = user_data["USER_EMAIL"]
        except:
            user_data = get_user_info_from_user()
            json.dump(user_data, config_file, indent=4)
            USER_NAME = user_data["USER_NAME"]
            USER_EMAIL = user_data["USER_EMAIL"]

#########################################################################
# LOCAL Config
#########################################################################

# Check if the ".neuq" folder exists, and if not, create it
if not os.path.exists(neuq_local_folder):
    os.mkdir(neuq_local_folder)

# if not os.path.exists(os.path.join(neuq_local_folder, neuq_local_config)):
#     with open(os.path.join(neuq_local_folder, neuq_local_config), "w") as config_file:
#         config_data = {
#             "directory": os.getcwd(),
#             "slides": [],
#         }
#         json.dump(config_data, config_file, indent=4)


#########################################################################
# APIs: Default
#########################################################################


@app.route("/")
def serve_index():
    """Serves the index.html file"""
    print("serving index.html")
    return send_from_directory("build", "index.html")


@app.route("/static/<path:static_path>")
def serve_static(static_path):
    """Serves static files from the build/static folder"""
    print("serving static")
    print(static_path)
    return send_from_directory("build/static", static_path)


# Service routes
@app.route("/api/essentials")
def get_essentials():
    """Returns the user name and email"""
    return jsonify({"user_name": USER_NAME, "user_email": USER_EMAIL})


#########################################################################
# CLASSES: Slides
#########################################################################


def generate_random_string():
    length = 8
    characters = (
        string.ascii_letters + string.digits
    )  # You can customize this to include other characters if needed
    random_string = "".join(random.choice(characters) for _ in range(length))
    random_string = random_string
    return random_string


class Slide:
    def __init__(
        self,
        title,
        order,
        canvas,
        filename,
    ):
        self.title = title
        self.order = order
        self.canvas = canvas
        self.filename = filename

    @classmethod
    def load(cls, filename):
        with open(os.path.join(neuq_local_folder, filename), "r") as slide_file:
            data = json.load(slide_file)
        return cls(data["title"], data["order"], data["canvas"], filename)

    @classmethod
    def new(cls, order=0):
        return cls(
            "Untitled",
            0,
            [],
            str(order) + "_" + generate_random_string() + neuq_slide_extension,
        )

    def setval(self, name, value):
        if hasattr(self, name):
            setattr(self, name, value)
        else:
            raise Exception(f"Attribute '{name}' does not exist")

    def getval(self, name):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            raise Exception(f"Attribute '{name}' does not exist")

    def save(self):
        with open(os.path.join(neuq_local_folder, self.filename), "w") as slide_file:
            slide_file.write(
                json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            )

    def changefilename(self, neworder):
        # Just replace the number and not the whole filename
        newfilename = neworder + "_" + self.filename.split("_", 1)[1]
        os.rename(
            os.path.join(neuq_local_folder, self.filename),
            os.path.join(neuq_local_folder, newfilename),
        )
        self.filename = newfilename


class Slides:
    def __init__(self, slides):
        self.slides = slides

    @classmethod
    def load(cls):
        slides = []
        filenames = [
            filename
            for filename in os.listdir(neuq_local_folder)
            if filename.endswith(neuq_slide_extension)
        ]
        filenames.sort()  # Sort the filenames alphabetically

        for filename in filenames:
            slides.append(Slide.load(filename))

        if len(slides) == 0:
            slide = Slide.new()
            slide.save()
            slides.append(slide)

        return cls(slides)

    def new_slide(self):
        # Get total number of slides
        total_slides = len(self.slides)
        slide = Slide.new(total_slides)
        slide.save()
        self.slides.append(slide)
        return slide.filename

    def consolidate_order(self):
        for index, slide in enumerate(self.slides):
            slide.changefilename(str(index))


#########################################################################
# APIs: Slides
#########################################################################

SLIDES = Slides.load()


# Slide APIs
@app.route("/api/slides/new", methods=["POST"])
def new_slide():
    """Adds a new slide to the current directory"""
    filename = SLIDES.new_slide()
    return jsonify({"filename": filename}), 201


@app.route("/api/slides/list")
def list_slides():
    """Returns a list of slides in the current directory"""
    return jsonify({"slides": [slide.filename for slide in SLIDES.slides]})


@app.route("/api/slides/delete/<int:index>", methods=["DELETE"])
def delete_slide(index):
    try:
        print(index)
        if 0 <= index < len(SLIDES.slides):
            deleted_slide = SLIDES.slides.pop(index)
            os.remove(os.path.join(neuq_local_folder, deleted_slide.filename))
            SLIDES.consolidate_order()

            return (
                jsonify({"message": f"Slide at index {index} deleted successfully"}),
                200,
            )
        else:
            return jsonify({"error": f"Invalid slide index {index}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/slides/save/<int:index>", methods=["POST"])
def save_slide(index):
    try:
        if 0 <= index < len(SLIDES.slides):
            saved_slide = SLIDES.slides[index]
            saved_slide.canvas = request.json.get("canvas")
            saved_slide.save()

            return (
                jsonify({"message": f"Slide at index {index} saved successfully"}),
                200,
            )
        else:
            return jsonify({"error": f"Invalid slide index {index}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#########################################################################
# APIs: Files
#########################################################################


@app.route("/files/list")
def list_files():
    """Returns a list of files in the current directory"""
    directory_path = "./"
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        files = os.listdir(directory_path)
        allowed_extensions = [".csv", ".jpg", ".jpeg", ".png"]
        filtered_files = [
            file
            for file in files
            if any(file.endswith(ext) for ext in allowed_extensions)
        ]
        return jsonify({"files": filtered_files})
    else:
        return jsonify({"error": "Directory not found"}), 404


@app.route("/files/use/<string:file_name>")
def use_files(file_name):
    """Returns the requested file data"""
    directory_path = "./"
    file_path = os.path.join(directory_path, file_name)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        file_extension = os.path.splitext(file_name)[-1].lower()

        if file_extension == ".csv":
            with open(file_path, "r") as csv_file:
                csv_data = csv_file.read()
                tab_separated_data = csv_data.replace(",", "\t")
            return jsonify(
                {"file_name": file_name, "data": tab_separated_data, "file_type": "csv"}
            )

        elif file_extension in [".jpg", ".jpeg", ".png"]:
            with open(file_path, "rb") as image_file:
                image_data = "data:image/png;base64," + base64.b64encode(
                    image_file.read()
                ).decode("utf-8")
            return jsonify(
                {"file_name": file_name, "data": image_data, "file_type": "image"}
            )
        else:
            return jsonify({"error": "Unsupported file type"}), 400
    else:
        return jsonify({"error": "File not found"}), 404


@app.route("/files/add/<string:file_name>", methods=["POST"])
def add_file(file_name):
    """Adds the dropped file to the current directory"""
    try:
        directory_path = "./"
        original_file_name = file_name
        file_path = os.path.join(directory_path, file_name)
        file_counter = 1

        # If the file already exists, modify the file name
        while os.path.exists(file_path):
            # Add an underscore and increment the counter
            file_name, file_extension = os.path.splitext(original_file_name)
            file_name = f"{file_name}_{file_counter}{file_extension}"
            file_path = os.path.join(directory_path, file_name)
            file_counter += 1

        file_extension = os.path.splitext(file_name)[-1].lower()

        if file_extension == ".csv":
            content = request.json.get("data")
            with open(file_path, "w") as file:
                file.write(content)

        elif file_extension in [".jpg", ".jpeg", ".png"]:
            # Get the Base64 encoded image data from the request
            image_data = request.json.get("data")

            # Remove the "data:image/[format];base64," prefix from the data
            _, encoded_data = image_data.split(",", 1)

            # Decode the Base64 data into binary image data
            image_binary = base64.b64decode(encoded_data)

            # Save the binary image data to the file
            with open(file_path, "wb") as image_file:
                image_file.write(image_binary)

        return (
            jsonify(
                {
                    "message": f"File '{file_name}' added successfully",
                    "file_name": file_name,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the application
if __name__ == "__main__":
    app.run(port=5380)
