import os
import secrets
from PIL import Image
from configs.default import UPLOAD_PROFILE_FOLDER

def save_image(image):
    random_hex = secrets.token_hex(8)
    name, ext = os.path.splitext(image.filename)
    picture_name = random_hex + ext

    output_size = (125, 125)
    i = Image.open(image)
    i.thumbnail(output_size)
    i.save(os.path.join(UPLOAD_PROFILE_FOLDER, picture_name))

    return picture_name