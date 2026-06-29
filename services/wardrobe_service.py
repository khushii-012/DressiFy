import os
from PIL import Image

WARDROBE_FOLDER = "assets/wardrobe"


def save_uploaded_image(uploaded_file):

    if uploaded_file is None:
        return ""

    if not os.path.exists(WARDROBE_FOLDER):
        os.makedirs(WARDROBE_FOLDER)

    filepath = os.path.join(
        WARDROBE_FOLDER,
        uploaded_file.name
    )

    image = Image.open(uploaded_file)
    image.save(filepath)

    return filepath