import logging
from pathlib import Path

from vlogging import HTMLFileHandler, VisualRecord

if __name__ == "__main__":
    import cv2
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image

    lenna = str(Path(__file__).parent / "vlogging" / "tests" / "lenna.jpg")

    # evenly sampled time at 200ms intervals
    t = np.arange(0., 5., 0.2)

    fig1 = plt.figure()
    plt.plot(t, t, 'r--', t, t ** 2, 'bs', t, t ** 3, 'g^')

    cv_image = cv2.imread(lenna)
    pil_image = Image.open(lenna)

    logger = logging.getLogger("demo")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(HTMLFileHandler("test.html", title="visual-logging demo"))

    logger.debug(VisualRecord(
        "Hello from OpenCV", cv_image, "This is OpenCV image", fmt="png"))

    logger.info(VisualRecord(
        "Hello from PIL", pil_image, "This is PIL image", fmt="jpeg"))

    logger.info(VisualRecord(
        "Hello from matplotlib", fig1, "This is matplotlib graph", fmt="png"))

    logger.warning(
        VisualRecord("Hello from all", [cv_image, pil_image, fig1],
                     fmt="png"))

    logger.warning(
        VisualRecord("Hello from all (downscaled to fit 200x200)",
                     [cv_image, pil_image, fig1],
                     fmt="png", max_size=(200, 200)))

    logger.info("Plain text records work too, and are escaped: <html> & so on")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception(VisualRecord(
            "Exceptions come with tracebacks", cv_image))

    logging.shutdown()
