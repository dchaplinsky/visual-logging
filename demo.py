from logging import FileHandler
from vlogging import VisualRecord

if __name__ == '__main__':
    import cv2
    from PIL import Image

    cv_image = cv2.imread('lenna.jpg')
    pil_image = Image.open('lenna.jpg')

    import logging
    logger = logging.getLogger("demo")
    fh = FileHandler('test.html', mode="w")

    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    logger.debug(VisualRecord(
        "Hello from OpenCV", cv_image, "multi\n\nline", fmt="png"))

    logger.info(VisualRecord(
        "Hello from PIL", pil_image, "annotation", fmt="jpeg"))

    logger.warning(
        VisualRecord("Hello from both", [cv_image, pil_image], fmt="jpeg"))
