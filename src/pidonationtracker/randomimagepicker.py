import os
import sys
import random

def pick_image(imagedir):
    """ Pick a random image from the image directory

    Args:
        scriptdir (str): directory from where the script is run

    Returns:
        ospath: location of the image
    """
    imagepath = os.path.join(imagedir, "images")
    image_list = os.listdir(imagepath)
    randomimage = random.choice(image_list)
    backgroundimage = os.path.join(imagepath, randomimage)
    return backgroundimage

if __name__ == "__main__":
    imagedir = os.path.abspath('.')
    # imagedir = os.path.join(basedir, "../../images")
    backgroundimage = pick_image(imagedir)
    print(f"Random image: {backgroundimage}")
