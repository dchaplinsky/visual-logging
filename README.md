visual-logging
==============

A simple way to generate beautiful html logs with embedded images for CV purposes.

visual-logging piggy backs on logging module and allows you to use sick power of logging to debug your computer vision application on a whole new level.

You can add OpenCV images (well technically it's numpy arrays) and PIL images to your logs. Matplotlib will be added as well.

## Installation
```pip install visuallloging```

No extra dependencies

## Usage example (see demo.py)
```python
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

```

You can generated html [here](http://dchaplinsky.github.io/visual-logging/)
