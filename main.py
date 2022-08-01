import os

import piexif
import re


def get_images(path="/home/arek/PycharmProjects/Dexiffer/Data"):
    list_of_images = []
    valid_extension = [".jpg", ".png", ".tiff"]
    for file in os.listdir(path):
        extension = os.path.splitext(file)[1]
        if extension.lower() not in valid_extension:
            continue
        list_of_images.append(os.path.join(path, file))
    return list_of_images


# removing 'b*'
def valid_string(name):
    fixed_string = re.sub(r"b\'([\w\d\s\.\-/]+)\'", r'\1', name)
    return fixed_string


def print_lens_model():
    files = get_images()
    for file in files:
        image = piexif.load(file)
        device = valid_string(str(image["0th"][272]))
        try:
            print(f"{device}:\n", valid_string(str(image["Exif"][42036])))
        except:
            print(f"For {device}", "lens model not available ")


print_lens_model()
