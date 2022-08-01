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
    valid_extension = [".jpg", ".png", ".tiff", ".rw2", ".dng"]
    try:
        for image_file in os.listdir(path_to_file):
            name = os.path.splitext(image_file)[0]
            extension = os.path.splitext(image_file)[1]
            if extension.lower() not in valid_extension:
                continue
            if name not in list_of_images:
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
    if not isinstance(name, str):
        raise TypeError
    fixed_string = re.sub(r"b'([\w\d\s.\-/|()]+)'", r'\1', name)
    return fixed_string


# When exif data key does not exist, default value = None
def valid_ifd_key(image_data):
    if image_data is None:
        return False
    else:
        # if not isinstance(image_data, str) or not isinstance(image_data, int):
        #     raise TypeError
        #     pass
        return True


# Access the details of a single exif data cell
def get_exif_data(particular_image, key, value):
    try:
        if valid_ifd_key(particular_image[key][value]):
            particular_device = valid_string(str(particular_image["0th"][272]))
            try:
                if value == 40962 or value == 40963:
                    return int(particular_image[key][value])
                return valid_string(str(particular_image[key][value]))
            except KeyError:
                print(f"For {particular_device}", "exif data not available ")
        else:
            return None
    except KeyError:
        # print(f"key error for {value}")
        return ""


def how_much_cropped(list_of_resolution):
    default_resolution = max(list_of_resolution)
    number_of_items = len(list_of_resolution)
    cropped_resolution = 0
    for particular_resolution in list_of_resolution:
        if particular_resolution != default_resolution:
            cropped_resolution += 1
    return str(round((cropped_resolution / number_of_items * 100))) if cropped_resolution != 0 else "0"


# creating the bar plot
def visualise_data(list_of_items, name_of_chart, flag=False, percentage_of_cropped=None):
    elements = collections.Counter(list_of_items)
    result = collections.OrderedDict(elements.most_common())
    keys = list(result.keys())
    values = list(result.values())
    if flag:
        keys = list(elements.keys())
        values = list(elements.values())
        if percentage_of_cropped != "0":
            plt.xlabel(f"Percentage of cropped photos: {percentage_of_cropped}%")
        else:
            plt.xlabel(f"No cropped photos found")
    plt.bar(keys, values, color="deepskyblue", width=0.5, align="center")
    plt.ylabel("Quantity")

    plt.title(name_of_chart)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()


# def filter_displaying_one_item(list_of_items):


if __name__ == '__main__':

    path = get_path()
    files = get_images(path)
    data = {"Manufacturer": [], "Device": [], "Lens": [], "ISO": [], "Edited with": [], "Resolution": []}
    resolution_per_device = {}

    for file in files:
        image = piexif.load(file)

        manufacturer = get_exif_data(image, "0th", 271)
        device = get_exif_data(image, "0th", 272)
        lens = get_exif_data(image, "Exif", 42036)
        iso = get_exif_data(image, "Exif", 34855)
        edit = get_exif_data(image, "0th", 305)

        data["Manufacturer"].append(manufacturer)
        data["Device"].append(device)
        data["Lens"].append(lens)
        data["ISO"].append(iso)
        data["Edited with"].append(edit)
        if isinstance(get_exif_data(image, "Exif", 40962), int) and isinstance(get_exif_data(image, "Exif", 40963),
                                                                               int):
            resolution = get_exif_data(image, "Exif", 40962) * get_exif_data(image, "Exif", 40963)
            if device not in resolution_per_device:
                resolution_per_device.update({device: []})
            resolution_per_device[device].append(str(round(resolution / 1000000, 4)))
            data["Resolution"].append(str(round(resolution / 1000000)))

    print(resolution_per_device)
    for item in data:
        if item == "ISO" or item == "Resolution":
            data[item].sort()
            visualise_data(data[item], item, True)
        else: visualise_data(data[item], item)
    for device_model in resolution_per_device:
        resolution_per_device[device_model].sort()
        visualise_data(resolution_per_device[device_model], device_model, True,
                       how_much_cropped(resolution_per_device[device_model]))
