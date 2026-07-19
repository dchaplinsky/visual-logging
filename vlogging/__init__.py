"""Embed OpenCV / PIL / matplotlib images into standard logging as HTML."""

from __future__ import annotations

import base64
import html
import logging
from io import BytesIO
from typing import Any, Optional

__version__ = "2.0"

__all__ = ["VisualRecord", "VisualFormatter", "HTMLFileHandler", "renderers"]

RenderResult = Optional["tuple[bytes, str]"]

renderers = []


def _fit_scale(width: float, height: float,
               max_size: tuple[int, int] | None) -> float:
    """Shrink-only scale factor that fits width x height into max_size."""
    if max_size is None:
        return 1

    return min(max_size[0] / width, max_size[1] / height, 1)


try:
    import cv2
    import numpy

    def render_opencv(img: Any, fmt: str = "png",
                      max_size: tuple[int, int] | None = None) -> RenderResult:
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

    def render_pil(img: Any, fmt: str = "png",
                   max_size: tuple[int, int] | None = None) -> RenderResult:
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
    import numpy
    from PIL import Image

    def render_numpy(img: Any, fmt: str = "png",
                     max_size: tuple[int, int] | None = None) -> RenderResult:
        # Fallback for numpy arrays when OpenCV is not installed (arrays are
        # assumed to be RGB; with OpenCV present, render_opencv wins and
        # treats them as BGR, as this library always did)
        if not isinstance(img, numpy.ndarray):
            return None

        try:
            return render_pil(Image.fromarray(img), fmt, max_size)
        except (TypeError, ValueError):
            return None

    renderers.append(render_numpy)
except ImportError:
    pass

try:
    import matplotlib  # noqa: F401

    def render_matplotlib(fig: Any, fmt: str = "png",
                          max_size: tuple[int, int] | None = None
                          ) -> RenderResult:
        if not callable(getattr(fig, "savefig", None)):
            return None

        kwargs = {}
        if max_size is not None:
            # fig may also be the pyplot module: measure its current figure
            sized = fig.gcf() if callable(getattr(fig, "gcf", None)) else fig
            if hasattr(sized, "get_size_inches"):
                dpi = sized.get_dpi()
                width, height = sized.get_size_inches() * dpi
                scale = _fit_scale(width, height, max_size)
                if scale < 1:
                    kwargs["dpi"] = dpi * scale

        output = BytesIO()
        fig.savefig(output, format=fmt, **kwargs)

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

    ``imgs`` accepts a single image or a list of OpenCV/numpy arrays, PIL
    images and matplotlib figures, in any combination. ``max_size`` is an
    optional ``(width, height)`` bound: images larger than that are
    downscaled (preserving aspect ratio) before being embedded, to keep log
    files small; matplotlib figures are downscaled by lowering the render
    dpi. ``title`` and ``footnotes`` are embedded as-is, so they may contain
    markup.

    Also renders itself in Jupyter notebooks via ``_repr_html_``.
    """

    def __init__(self, title: str = "", imgs: Any = None, footnotes: str = "",
                 fmt: str = "png",
                 max_size: tuple[int, int] | None = None) -> None:
        self.title = title
        self.fmt = fmt
        self.max_size = max_size

        if imgs is None:
            imgs = []

        self.imgs = imgs

        if not isinstance(imgs, (list, tuple, set, frozenset)):
            self.imgs = [self.imgs]

        self.footnotes = footnotes

    def render_images(self) -> str:
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
            '<img src="data:%s;base64,%s" loading="lazy" />' %
            (mime, base64.b64encode(data).decode())
            for data, mime in rendered)

    def render_footnotes(self) -> str:
        if not self.footnotes:
            return ""

        return f"<pre>{self.footnotes}</pre>"

    def html(self) -> str:
        """The record as an HTML fragment, without the trailing rule."""
        return (
            f"""
            <h4>{self.title}</h4>
            {self.render_images()}
            {self.render_footnotes()}""")

    _repr_html_ = html

    def __str__(self) -> str:
        return self.html() + "\n            <hr/>"


class VisualFormatter(logging.Formatter):
    """Formats log records as styled HTML cards.

    ``VisualRecord`` messages get their images embedded; any other message
    is escaped and rendered as text, so ordinary log calls mix in safely.
    Meant for handlers that write to an html page, e.g. ``HTMLFileHandler``
    (which installs it by default).
    """

    def format(self, record: logging.LogRecord) -> str:
        if isinstance(record.msg, VisualRecord):
            body = record.msg.html()
        else:
            body = f"<pre>{html.escape(record.getMessage())}</pre>"

        if record.exc_info:
            body += ('\n<pre class="traceback">%s</pre>' %
                     html.escape(self.formatException(record.exc_info)))

        if record.stack_info:
            body += ('\n<pre class="traceback">%s</pre>' %
                     html.escape(self.formatStack(record.stack_info)))

        levelclass = "".join(
            c for c in record.levelname.lower() if c.isalnum())

        return (
            '<article class="record %s">\n'
            '<header><span class="level">%s</span>'
            '<span class="logger">%s</span>'
            '<time>%s</time></header>%s\n'
            '</article>' % (
                levelclass,
                html.escape(record.levelname),
                html.escape(record.name),
                html.escape(self.formatTime(record, self.datefmt)),
                body,
            ))


_PAGE_HEADER = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>
:root { color-scheme: light dark; }
body {
    margin: 0 auto; padding: 1rem; max-width: 60rem;
    font-family: system-ui, sans-serif;
}
.record {
    border: 1px solid #8884; border-left: .25rem solid var(--accent, #888);
    border-radius: .25rem; padding: .5rem .75rem; margin: .75rem 0;
}
.record.debug { --accent: #9e9e9e; }
.record.info { --accent: #2196f3; }
.record.warning { --accent: #ff9800; }
.record.error { --accent: #f44336; }
.record.critical { --accent: #b71c1c; }
.record > header {
    display: flex; gap: .75rem; align-items: baseline;
    font-size: .8rem; margin-bottom: .25rem;
}
.record .level { color: var(--accent); font-weight: 700; }
.record .logger { opacity: .7; }
.record time {
    margin-left: auto; opacity: .7; font-variant-numeric: tabular-nums;
}
.record h4 { margin: .25rem 0; }
.record img { max-width: 100%%; height: auto; margin: .25rem .25rem 0 0; }
.record pre {
    overflow-x: auto; background: #8881;
    padding: .5rem; border-radius: .25rem;
}
.record hr { display: none; }
</style>
</head>
<body>
<main>
"""

_PAGE_FOOTER = "</main>\n</body>\n</html>\n"


class HTMLFileHandler(logging.FileHandler):
    """A ``logging.FileHandler`` that writes a self-contained html page.

    Writes the page header (with embedded CSS) when the file is opened,
    formats records with ``VisualFormatter`` unless another formatter is
    set, and closes the page on ``close()`` / ``logging.shutdown()``.
    Records are flushed as they are emitted, so the page can be watched
    while the program is still running.

    Unlike ``FileHandler``, the default mode is ``"w"``: a log page is
    normally rewritten per run.
    """

    def __init__(self, filename: Any, mode: str = "w",
                 encoding: str | None = "utf-8", delay: bool = False,
                 title: str = "Log") -> None:
        self.title = title
        super().__init__(filename, mode=mode, encoding=encoding, delay=delay)
        self.setFormatter(VisualFormatter())

    def _open(self):
        stream = super()._open()
        if stream.tell() == 0:
            stream.write(_PAGE_HEADER % html.escape(self.title))

        return stream

    def close(self) -> None:
        if self.stream and not self.stream.closed:
            self.acquire()
            try:
                self.stream.write(_PAGE_FOOTER)
            finally:
                self.release()

        super().close()
