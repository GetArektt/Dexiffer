import os

import piexif
import re

default_path = os.getcwd()



def get_images(path=None):
    if path is None or path == "n":
        path = default_path + "/Data"
    list_of_images = []
    valid_extension = [".jpg", ".png", ".tiff"]
    try:
        for file in os.listdir(path):
            extension = os.path.splitext(file)[1]
            if extension.lower() not in valid_extension:
                continue
            list_of_images.append(os.path.join(path, file))
    except:
        print("Error")
    return list_of_images


# suitable format: /example/path/images, "n" for default path
def get_path():
    path = str(input("Please enter the path:\n"))
    if path == "\n":
        path = None
    return path


# converting 'bexample_name' -> example_name
def valid_string(name):
    fixed_string = re.sub(r"b\'([\w\d\s.\-/\|]+)\'", r'\1', name)
    return fixed_string


# When exif data key does not exist, default value = None
def valid_ifd_key(data):
    if data is None:
        return False
    else:
        return True


def print_lens_model():
    path = get_path()
    files = get_images(path)
    for file in files:
        image = piexif.load(file)
        try:
            if valid_ifd_key(image["0th"][272]):
                device = valid_string(str(image["0th"][272]))
            try:
                print(f"{device}:\n", valid_string(str(image["Exif"][42036])))
            except:
                print(f"For {device}", "lens model not available ")
        except:
            pass


print_lens_model()
