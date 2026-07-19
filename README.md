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

No extra dependencies — whichever of OpenCV, PIL/Pillow and matplotlib you already have installed are picked up automatically (numpy arrays render through PIL when OpenCV isn't around). Requires Python 3.9+.

## Usage example (see demo.py)

```python
import logging
from vlogging import HTMLFileHandler, VisualRecord

import cv2  # or PIL.Image, or matplotlib — whatever you use

logger = logging.getLogger("demo")
logger.setLevel(logging.DEBUG)
logger.addHandler(HTMLFileHandler("test.html", title="My debug log"))

cv_image = cv2.imread("lenna.jpg")

logger.debug(VisualRecord(
    "Hello from OpenCV", cv_image, "This is an OpenCV image", fmt="png"))

# Mix images of different origins in one record, downscale the big ones
# to at most 320x240 to keep the log small:
logger.warning(VisualRecord(
    "Hello from all", [cv_image, pil_image, mpl_figure],
    fmt="png", max_size=(320, 240)))

# Ordinary log calls work too, and land in the same page:
logger.info("Processed frame %d", 42)

logging.shutdown()  # flushes and closes the html file
```

Open `test.html` in a browser and enjoy: `HTMLFileHandler` writes a styled, self-contained page — records are color-coded by log level with timestamps and logger names, plain messages are escaped, and exceptions logged with `logger.exception(...)` include their traceback. Records are flushed as they happen, so you can watch the page mid-run.

Everything composes the stdlib way: `HTMLFileHandler` is a `logging.FileHandler` that installs a `VisualFormatter` (a `logging.Formatter`) by default — use either piece on its own if you prefer. Passing a `VisualRecord` to a plain `FileHandler` still produces bare html fragments, exactly as in 1.x.

In **Jupyter**, a `VisualRecord` displays itself inline — no logging setup needed:

```python
VisualRecord("Detected edges", edges_img, "Canny output")
```

### `VisualRecord` arguments

| Argument | Meaning |
| --- | --- |
| `title` | Header of the log record |
| `imgs` | A single image or a list of images: OpenCV/numpy arrays, PIL images and matplotlib figures in any combination |
| `footnotes` | Optional text rendered as `<pre>` under the images |
| `fmt` | Image format to embed: `png` (default), `jpeg`, `webp` — anything your imaging library can encode |
| `max_size` | Optional `(width, height)` tuple: images bigger than that are downscaled proportionally before embedding (matplotlib figures by lowering the render dpi), to keep log files readable and small |

## Changelog

**2.0**
- Modern packaging (`pyproject.toml`), Python 3.9+ only, `py.typed` type hints
- New `HTMLFileHandler` + `VisualFormatter`: styled, self-contained html pages with level colors, timestamps, escaped plain-text records and tracebacks
- New `max_size` option to downscale embedded images (all renderers)
- `VisualRecord` displays inline in Jupyter notebooks
- numpy arrays render via PIL when OpenCV is not installed
- Embedded images use `loading="lazy"`, so huge logs open fast
- matplotlib support no longer relies on the deprecated `pylab` module
- Tests run on GitHub Actions against Python 3.9–3.13; releases publish to PyPI from tags via trusted publishing
