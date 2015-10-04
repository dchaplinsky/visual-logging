# -*- coding: utf-8 -*-

from io import BytesIO as StringIO
from string import Template
import base64

__version__ = "0.2"
renderers = []

try:
    import cv2
    import numpy

    def render_opencv(img, fmt="png"):
        if not isinstance(img, numpy.ndarray):
            return None

        retval, buf = cv2.imencode(".%s" % fmt, img)
        if not retval:
            return None

        return buf, "image/%s" % fmt

    renderers.append(render_opencv)
except ImportError:
    pass

try:
    from PIL import Image

    def render_pil(img, fmt="png"):
        if not callable(getattr(img, "save", None)):
            return None

        output = StringIO()
        img.save(output, format=fmt)
        contents = output.getvalue()
        output.close()

        return contents, "image/%s" % fmt

    renderers.append(render_pil)
except ImportError:
    pass

try:
    import pylab

    def render_pylab(img, fmt="png"):
        if not callable(getattr(img, "savefig", None)):
            return None

        output = StringIO()
        img.savefig(output, format=fmt)
        contents = output.getvalue()
        output.close()

        return contents, "image/%s" % fmt

    renderers.append(render_pylab)
except ImportError:
    pass


class VisualRecord(object):
    def __init__(self, title="", imgs=None, footnotes="", fmt="png"):
        self.title = title
        self.fmt = fmt

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
                res = renderer(img, self.fmt)

                if res is None:
                    continue
                else:
                    rendered.append(res)
                    break

        return "".join(
            Template('<img src="data:$mime;base64,$data" />').substitute({
                "data": base64.b64encode(data),
                "mime": mime
            }) for data, mime in rendered)

    def render_footnotes(self):
        if not self.footnotes:
            return ""

        return Template("<pre>$footnotes</pre>").substitute({
            "footnotes": self.footnotes
        })

    def __str__(self):
        t = Template(
            """
            <h4>$title</h4>
            $imgs
            $footnotes
            <hr/>""")

        return t.substitute({
            "title": self.title,
            "imgs": self.render_images(),
            "footnotes": self.render_footnotes()
        })
