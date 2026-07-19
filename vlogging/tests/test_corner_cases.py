import sys
import unittest
from unittest import mock


class CornerCasesTestCase(unittest.TestCase):
    def test_no_renderers(self):
        # None in sys.modules makes imports of the imaging libraries raise
        # ImportError; patch.dict restores the real modules (and the original
        # vlogging, dropped inside the block) afterwards
        blocked = dict.fromkeys(("cv2", "numpy", "PIL", "matplotlib"))
        with mock.patch.dict(sys.modules, blocked):
            sys.modules.pop("vlogging", None)

            import vlogging
            self.assertEqual(vlogging.renderers, [])
