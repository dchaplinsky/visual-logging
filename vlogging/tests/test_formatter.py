import logging
import tempfile
import unittest
from pathlib import Path

import vlogging


class HTMLFileHandlerTestCase(unittest.TestCase):
    def render_log(self, emit, **handler_kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "log.html"
            handler = vlogging.HTMLFileHandler(str(path), **handler_kwargs)

            logger = logging.Logger("demo")
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)

            emit(logger)
            handler.close()

            return path.read_text(encoding="utf-8")

    def test_page_structure(self):
        s = self.render_log(lambda logger: logger.info("hello"),
                            title="my <log>")

        self.assertTrue(s.startswith("<!doctype html>"))
        self.assertTrue("<style>" in s)
        self.assertTrue("<title>my &lt;log&gt;</title>" in s)
        self.assertTrue(s.rstrip().endswith("</html>"))

    def test_plain_messages_escaped(self):
        s = self.render_log(
            lambda logger: logger.info("careful with <b>%s</b> & co", "this"))

        self.assertTrue("careful with &lt;b&gt;this&lt;/b&gt; &amp; co" in s)
        self.assertTrue('class="record info"' in s)
        self.assertTrue('<span class="logger">demo</span>' in s)

    def test_visual_record(self):
        from PIL import Image

        lenna = Image.open(Path(__file__).parent / "lenna.jpg")
        s = self.render_log(lambda logger: logger.warning(
            vlogging.VisualRecord("title", lenna, "notes")))

        self.assertTrue('class="record warning"' in s)
        self.assertEqual(s.count("<img"), 1)
        self.assertTrue("data:image/png;base64" in s)

    def test_exception(self):
        def emit(logger):
            try:
                1 / 0
            except ZeroDivisionError:
                logger.exception("boom")

        s = self.render_log(emit)

        self.assertTrue('class="record error"' in s)
        self.assertTrue("ZeroDivisionError" in s)
        self.assertTrue('class="traceback"' in s)

    def test_no_duplicate_footer_on_double_close(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "log.html"
            handler = vlogging.HTMLFileHandler(str(path))
            handler.close()
            handler.close()

            self.assertEqual(path.read_text(encoding="utf-8").count("</html>"), 1)
