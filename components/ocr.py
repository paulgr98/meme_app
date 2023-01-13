import pytesseract as tess
from PIL import Image


def set_tesseract_path(path: str) -> None:
    tess.pytesseract.tesseract_cmd = path


def get_image(path: str) -> Image:
    original_image = Image.open(path)
    # convert to grayscale
    grayscale_image = original_image.convert('L')
    # make image larger, so that text is easier to read for tesseract
    grayscale_image = grayscale_image.resize((grayscale_image.width * 2, grayscale_image.height * 2))
    return grayscale_image


def get_text(image: Image) -> list[str]:
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


# TODO: implement OpenCV YOLO object detection
def get_objects_from_image(self, path: str) -> list[str]:
    pass
