visual-logging
==============

[![Tests](https://github.com/dchaplinsky/visual-logging/actions/workflows/tests.yml/badge.svg)](https://github.com/dchaplinsky/visual-logging/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/visual-logging.svg)](https://pypi.org/project/visual-logging/)

A simple way to generate beautiful html logs with embedded images for CV purposes.

visual-logging piggybacks on the standard `logging` module and allows you to use the sick power of logging to debug your computer vision application on a whole new level: OpenCV images (well, technically numpy arrays), PIL images and matplotlib figures get embedded into your html logs as inline images.

You can read about it in detail in a great blog post [visual-logging, my new favorite tool for debugging OpenCV and Python apps](http://www.pyimagesearch.com/2014/12/22/visual-logging-new-favorite-tool-debugging-opencv-python-apps/) written by Adrian Rosebrock.

## Installation

```
pip install visual-logging
```

No extra dependencies — whichever of OpenCV, PIL/Pillow and matplotlib you already have installed are picked up automatically. Requires Python 3.9+.

## Usage example (see demo.py)

```python
import logging
from logging import FileHandler
from vlogging import VisualRecord

import cv2  # or PIL.Image, or matplotlib — whatever you use

logger = logging.getLogger("demo")
logger.setLevel(logging.DEBUG)
logger.addHandler(FileHandler("test.html", mode="w"))

cv_image = cv2.imread("lenna.jpg")

logger.debug(VisualRecord(
    "Hello from OpenCV", cv_image, "This is an OpenCV image", fmt="png"))

# Mix images of different origins in one record, downscale the big ones
# to at most 320x240 to keep the log small:
logger.warning(VisualRecord(
    "Hello from all", [cv_image, pil_image, mpl_figure],
    fmt="png", max_size=(320, 240)))

logging.shutdown()  # flushes and closes the html file
```

Open `test.html` in a browser and enjoy. A sample of generated html is available [here](http://dchaplinsky.github.io/visual-logging/).

### `VisualRecord` arguments

| Argument | Meaning |
| --- | --- |
| `title` | Header of the log record |
| `imgs` | A single image or a list of images: OpenCV/numpy arrays, PIL images and matplotlib figures in any combination |
| `footnotes` | Optional text rendered as `<pre>` under the images |
| `fmt` | Image format to embed: `png` (default), `jpeg`, `webp` — anything your imaging library can encode |
| `max_size` | Optional `(width, height)` tuple: raster images bigger than that are downscaled proportionally before embedding, to keep log files readable and small |

## Changelog

**2.0**
- Modern packaging (`pyproject.toml`), Python 3.9+ only
- New `max_size` option to downscale embedded images
- matplotlib support no longer relies on the deprecated `pylab` module
- Tests run on GitHub Actions against Python 3.9–3.13
