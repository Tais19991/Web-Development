import colorgram
from PIL import Image
import os

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def find_img_colors(img_file_path: str) -> dict:
    # image processing
    img = Image.open(img_file_path).convert('RGB')
    colors = colorgram.extract(img, 10)
    color_dict = {}
    for color in colors:
        rgb = color.rgb
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        color_tuple = (red, green, blue)
        color_dict['#{:02x}{:02x}{:02x}'.format(red, green, blue)] = color_tuple
    return color_dict


def get_file_path(file_name: str) -> str:
    file_path = os.path.join('static/uploads', file_name)
    return file_path
