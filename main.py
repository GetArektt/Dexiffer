import os

import piexif
import re

import pandas as pd

default_path = os.getcwd()


# load only files with image extensions such as .jpg/.png
def get_images(path_to_file=None):
    if path_to_file is None or path_to_file == "n":
        path_to_file = default_path + "/Data"
    list_of_images = []
    valid_extension = [".jpg", ".png", ".tiff"]
    try:
        for image_file in os.listdir(path_to_file):
            extension = os.path.splitext(image_file)[1]
            if extension.lower() not in valid_extension:
                continue
            list_of_images.append(os.path.join(path_to_file, image_file))
    except:
        print("Error")
    return list_of_images


# suitable format: /example/path/images, "n" for default path
def get_path():
    path_to_file = str(input("Please enter the path:\n"))
    if path_to_file == "\n":
        path_to_file = None
    return path_to_file


# converting 'bexample_name' -> example_name
def valid_string(name):
    fixed_string = re.sub(r"b\'([\w\d\s.\-/|]+)\'", r'\1', name)
    return fixed_string


# When exif data key does not exist, default value = None
def valid_ifd_key(image_data):
    if image_data is None:
        return False
    else:
        return True


def print_exif_data(particular_image, key, value):
    try:
        if valid_ifd_key(particular_image[key][value]):
            particular_device = valid_string(str(particular_image["0th"][272]))
            try:
                return valid_string(str(particular_image[key][value]))
            except:
                print(f"For {particular_device}", "exif data not available ")
        else:
            return None
    except KeyError:
        print("key error")
        return None


if __name__ == '__main__':
    path = get_path()
    files = get_images(path)
    for file in files:
        image = piexif.load(file)
        manufacturer = print_exif_data(image, "0th", 271)
        device = print_exif_data(image, "0th", 272)
        lens = print_exif_data(image, "Exif", 42036)
        iso = print_exif_data(image, "Exif", 34855)
        edit = print_exif_data(image, "0th", 305)
        # resolution = ()                                                                                                #Add later
        data = {"Manufacturer": manufacturer, "Device": device, "Lens": lens, "ISO": [iso], "Edited with": edit}
        df = pd.DataFrame(data)
        print(df)
