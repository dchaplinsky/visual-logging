import unittest
from pathlib import Path

import vlogging

LENNA = str(Path(__file__).parent / "lenna.jpg")


class BasicTestCase(unittest.TestCase):
    def test_nothing(self):
        s = str(vlogging.VisualRecord())
        self.assertTrue("<hr/>" in s)

    def test_text_only(self):
        s = str(vlogging.VisualRecord(title="title", footnotes="footnotes"))
        self.assertTrue("title" in s)
        self.assertTrue("footnotes" in s)
        self.assertTrue("<pre>" in s)

    def test_all_renderers(self):
        self.assertEqual(len(vlogging.renderers), 3)

    def test_invalid_images(self):
        s = str(vlogging.VisualRecord(
            title="title",
            imgs="foobar",
            footnotes="footnotes"))

        self.assertTrue("title" in s)
        self.assertTrue("footnotes" in s)
        self.assertTrue("<pre>" in s)
        self.assertEqual(s.count("<img"), 0)

        s = str(vlogging.VisualRecord(
            title="title",
            imgs=["foobar", 1, 2, dict()],
            footnotes="footnotes"))

        self.assertTrue("title" in s)
        self.assertTrue("footnotes" in s)
        self.assertTrue("<pre>" in s)
        self.assertEqual(s.count("<img"), 0)

    def test_pil(self):
        from PIL import Image

        pil_image = Image.open(LENNA)
        s = str(vlogging.VisualRecord(
            title="title",
            imgs=pil_image,
            footnotes="footnotes"))

        self.assertTrue("title" in s)
        self.assertTrue("footnotes" in s)
        self.assertTrue("<pre>" in s)
        self.assertTrue("image/png" in s)
        self.assertEqual(s.count("<img"), 1)

        s = str(vlogging.VisualRecord(
            title="title",
            imgs=[pil_image],
            footnotes="footnotes"))

        self.assertEqual(s.count("<img"), 1)

        s = str(vlogging.VisualRecord(
            title="title",
            imgs=[pil_image, pil_image],
            footnotes="footnotes",
            fmt="jpeg"))

        self.assertTrue("image/jpeg" in s)
        self.assertEqual(s.count("<img"), 2)

    def test_pil_max_size(self):
        from io import BytesIO

        from PIL import Image

        pil_image = Image.open(LENNA)

        resized, mime = vlogging.render_pil(pil_image, max_size=(64, 64))
        self.assertEqual(mime, "image/png")
        restored = Image.open(BytesIO(resized))
        self.assertTrue(max(restored.size) <= 64)

        # Image already fits: rendered as is
        same, _ = vlogging.render_pil(pil_image, max_size=(10000, 10000))
        restored = Image.open(BytesIO(same))
        self.assertEqual(restored.size, pil_image.size)

    def test_opencv(self):
        import cv2

        cv_image = cv2.imread(LENNA)
        s = str(vlogging.VisualRecord(
            title="title",
            imgs=cv_image,
            footnotes="footnotes"))

        self.assertTrue("title" in s)
        self.assertTrue("footnotes" in s)
        self.assertTrue("<pre>" in s)
        self.assertEqual(s.count("<img"), 1)

        s = str(vlogging.VisualRecord(
            title="title",
            imgs=[cv_image],
            footnotes="footnotes"))

        self.assertEqual(s.count("<img"), 1)

        s = str(vlogging.VisualRecord(
            title="title",
            imgs=[cv_image, cv_image],
            footnotes="footnotes"))

        self.assertEqual(s.count("<img"), 2)

    def test_opencv_max_size(self):
        import cv2
        import numpy

        cv_image = cv2.imread(LENNA)

        resized, mime = vlogging.render_opencv(cv_image, max_size=(64, 64))
        self.assertEqual(mime, "image/png")
        restored = cv2.imdecode(
            numpy.frombuffer(bytes(resized), numpy.uint8), cv2.IMREAD_COLOR)
        self.assertTrue(max(restored.shape[:2]) <= 64)

        # Image already fits: rendered as is
        same, _ = vlogging.render_opencv(cv_image, max_size=(10000, 10000))
        restored = cv2.imdecode(
            numpy.frombuffer(bytes(same), numpy.uint8), cv2.IMREAD_COLOR)
        self.assertEqual(restored.shape, cv_image.shape)

    def test_matplotlib_basic(self):
        import matplotlib.pyplot as plt
        import numpy as np

        t = np.arange(0., 5., 0.2)

        plt.plot(t, t, 'r--', t, t ** 2, 'bs', t, t ** 3, 'g^')

        s = str(vlogging.VisualRecord(
            title="title",
            imgs=plt,
            footnotes="footnotes"))

        self.assertTrue("title" in s)
        self.assertTrue("footnotes" in s)
        self.assertTrue("<pre>" in s)
        self.assertEqual(s.count("<img"), 1)

    def test_matplotlib_figure(self):
        import matplotlib.pyplot as plt
        import numpy as np

        t = np.arange(0., 5., 0.2)

        fig = plt.figure()
        plt.plot(t, t, 'r--', t, t ** 2, 'bs', t, t ** 3, 'g^')

        s = str(vlogging.VisualRecord(
            title="title",
            imgs=fig,
            footnotes="footnotes"))

        self.assertTrue("title" in s)
        self.assertTrue("footnotes" in s)
        self.assertTrue("<pre>" in s)
        self.assertEqual(s.count("<img"), 1)
