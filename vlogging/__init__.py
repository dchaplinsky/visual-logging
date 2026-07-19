"""Embed OpenCV / PIL / matplotlib images into standard logging as HTML."""

import base64
from io import BytesIO

__version__ = "2.0"

renderers = []


def _fit_scale(width, height, max_size):
    """Shrink-only scale factor that fits width x height into max_size."""
    if max_size is None:
        return 1

    return min(max_size[0] / width, max_size[1] / height, 1)


try:
    import cv2
    import numpy

    def render_opencv(img, fmt="png", max_size=None):
        if not isinstance(img, numpy.ndarray):
            return None

        scale = _fit_scale(img.shape[1], img.shape[0], max_size)
        if scale < 1:
            img = cv2.resize(img, None, fx=scale, fy=scale,
                             interpolation=cv2.INTER_AREA)

        retval, buf = cv2.imencode(f".{fmt}", img)
        if not retval:
            return None

        return buf, f"image/{fmt}"

    renderers.append(render_opencv)
except ImportError:
    pass

try:
    from PIL import Image

    def render_pil(img, fmt="png", max_size=None):
        if not isinstance(img, Image.Image):
            return None

        scale = _fit_scale(img.width, img.height, max_size)
        if scale < 1:
            img = img.resize((max(1, round(img.width * scale)),
                              max(1, round(img.height * scale))))

        output = BytesIO()
        img.save(output, format=fmt)

        return output.getvalue(), f"image/{fmt}"

    renderers.append(render_pil)
except ImportError:
    pass

try:
    import matplotlib  # noqa: F401

    def render_matplotlib(fig, fmt="png", max_size=None):
        if not callable(getattr(fig, "savefig", None)):
            return None

        output = BytesIO()
        fig.savefig(output, format=fmt)

        return output.getvalue(), f"image/{fmt}"

    renderers.append(render_matplotlib)

    # Name of the renderer prior to 2.0
    render_pylab = render_matplotlib
except ImportError:
    pass


class VisualRecord:
    """A log record that renders itself as HTML with embedded images.

    Pass it to any logger whose handler writes to an html file:

        logger.debug(VisualRecord("title", img, "notes"))

    ``imgs`` accepts a single image or a list of OpenCV arrays, PIL images
    and matplotlib figures, in any combination. ``max_size`` is an optional
    ``(width, height)`` bound: OpenCV and PIL images larger than that are
    downscaled (preserving aspect ratio) before being embedded, to keep log
    files small; matplotlib figures are embedded as rendered.
    """

    def __init__(self, title="", imgs=None, footnotes="", fmt="png",
                 max_size=None):
        self.title = title
        self.fmt = fmt
        self.max_size = max_size

        if imgs is None:
            imgs = []

        self.imgs = imgs

        if not isinstance(imgs, (list, tuple, set, frozenset)):
            self.imgs = [self.imgs]

        self.footnotes = footnotes

    def render_images(self):
        rendered = []

        for img in self.imgs:
            for renderer in renderers:
                # Trying renderers we have one by one
                res = renderer(img, self.fmt, self.max_size)

                if res is None:
                    continue
                else:
                    rendered.append(res)
                    break

        return "".join(
            '<img src="data:%s;base64,%s" />' %
            (mime, base64.b64encode(data).decode())
            for data, mime in rendered)

    def render_footnotes(self):
        if not self.footnotes:
            return ""

        return f"<pre>{self.footnotes}</pre>"

    def __str__(self):
        return (
            f"""
            <h4>{self.title}</h4>
            {self.render_images()}
            {self.render_footnotes()}
            <hr/>""")
