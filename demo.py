from logging import FileHandler
from vlogging import VisualRecord

if __name__ == '__main__':
    import cv2
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt

    # evenly sampled time at 200ms intervals
    t = np.arange(0., 5., 0.2)

    fig1 = plt.figure()
    plt.plot(t, t, 'r--', t, t ** 2, 'bs', t, t ** 3, 'g^')

    cv_image = cv2.imread('vlogging/tests/lenna.jpg')
    pil_image = Image.open('vlogging/tests/lenna.jpg')

    import logging
    logger = logging.getLogger("demo")
    fh = FileHandler('test.html', mode="w")

    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    logger.debug(VisualRecord(
        "Hello from OpenCV", cv_image, "This is openCV image", fmt="png", size=(50, 50)))

    logger.info(VisualRecord(
        "Hello from PIL", pil_image, "This is PIL image", fmt="jpeg", size=(100, 300)))

    logger.info(VisualRecord(
        "Hello from pylab", fig1, "This is PyLab graph", fmt="png", size=(100, 300)))

    logger.warning(
        VisualRecord("Hello from all", [cv_image, pil_image, fig1],
                     fmt="png", size=(50, 50)))
