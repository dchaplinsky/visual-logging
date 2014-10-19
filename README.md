visual-logging
==============

A simple way to generate beautiful html logs with embedded images for CV purposes.

visual-logging piggy backs on logging module and allows you to use sick power of logging to debug your computer vision application on a whole new level.

Now you can add OpenCV images (well technically it's numpy arrays), PIL images and matplotlib graphs to your logs.


[![Build Status](https://travis-ci.org/dchaplinsky/visual-logging.svg?branch=master)](https://travis-ci.org/dchaplinsky/visual-logging)
[![Coverage Status](https://coveralls.io/repos/dchaplinsky/visual-logging/badge.png)](https://coveralls.io/r/dchaplinsky/visual-logging)

## Installation
```pip install visual-logging```

No extra dependencies

## Usage example (see demo.py)
```python
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

    cv_image = cv2.imread('lenna.jpg')
    pil_image = Image.open('lenna.jpg')

    import logging
    logger = logging.getLogger("demo")
    fh = FileHandler('test.html', mode="w")

    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    logger.debug(VisualRecord(
        "Hello from OpenCV", cv_image, "This is openCV image", fmt="png"))

    logger.info(VisualRecord(
        "Hello from PIL", pil_image, "This is PIL image", fmt="jpeg"))

    logger.info(VisualRecord(
        "Hello from pylab", fig1, "This is PyLab graph", fmt="png"))

    logger.warning(
        VisualRecord("Hello from all", [cv_image, pil_image, fig1],
                     fmt="png"))

```

You can check generated html [here](http://dchaplinsky.github.io/visual-logging/)
