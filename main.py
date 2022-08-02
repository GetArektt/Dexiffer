import collections
import os
import re

import matplotlib.pyplot as plt
import piexif

default_path = os.getcwd()


# load only files with image extensions such as .jpg/.png
def get_images(path_to_file=None):
    if path_to_file is None or path_to_file == "n":
        path_to_file = default_path
    list_of_images = []
    valid_extension = [".jpg", ".png", ".tiff", ".rw2"]
    try:
        for image_file in os.listdir(path_to_file):
            extension = os.path.splitext(image_file)[1]
            if extension.lower() not in valid_extension:
                continue
            list_of_images.append(os.path.join(path_to_file, image_file))
    except os.error:
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
    fixed_string = re.sub(r"b'([\w\d\s.\-/|()]+)'", r'\1', name)
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
            except KeyError:
                print(f"For {particular_device}", "exif data not available ")
        else:
            return None
    except KeyError:
        print(f"key error for {value}")
        return "None"


# creating the bar plot
def visualise_data(list_of_items, name_of_chart):
    elements = collections.Counter(list_of_items)
    keys = list(elements.keys())
    values = list(elements.values())
    plt.bar(keys, values, color="deepskyblue", width=0.5, )
    plt.ylabel("Quantity")
    plt.title(name_of_chart)
    plt.show()


if __name__ == '__main__':
    path = get_path()
    files = get_images(path)
    data = {"Manufacturer": [], "Device": [], "Lens": [], "ISO": [], "Edited with": []}
    for file in files:
        image = piexif.load(file)
        manufacturer = print_exif_data(image, "0th", 271)
        data["Manufacturer"].append(manufacturer)
        device = print_exif_data(image, "0th", 272)
        data["Device"].append(device)
        lens = print_exif_data(image, "Exif", 42036)
        data["Lens"].append(lens)
        iso = print_exif_data(image, "Exif", 34855)
        data["ISO"].append(iso)
        edit = print_exif_data(image, "0th", 305)
        data["Edited with"].append(edit)

    for item in data:
        visualise_data(data[item], item)
