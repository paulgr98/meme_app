import pytesseract as tess
from PIL import Image


def set_tesseract_path(path):
    tess.pytesseract.tesseract_cmd = path


def get_image(path):
    original_image = Image.open(path)
    # convert to grayscale
    grayscale_image = original_image.convert('L')
    # make image larger, so that text is easier to read for tesseract
    grayscale_image = grayscale_image.resize((grayscale_image.width * 2, grayscale_image.height * 2))
    return grayscale_image


def get_text(image):
    text = tess.image_to_string(image)
    # remove newlines
    text = text.replace('\n', ',')
    # make into list
    text = text.split(',')
    # remove empty strings
    text = list(filter(None, text))
    # lowercase all strings
    text = [x.lower() for x in text]
    return text
