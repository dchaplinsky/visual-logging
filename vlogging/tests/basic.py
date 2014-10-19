import unittest

import sys

if sys.path[0].endswith("dummies"):
    sys.path = sys.path[1:]

import vlogging


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

        pil_image = Image.open('vlogging/tests/lenna.jpg')
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

    def test_opencv(self):
        import cv2

        cv_image = cv2.imread('vlogging/tests/lenna.jpg')
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

    def test_pylab_basic(self):
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

    def test_pylab_figure(self):
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
