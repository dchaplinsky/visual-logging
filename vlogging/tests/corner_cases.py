import os
import sys
import unittest

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "dummies"))
import vlogging


class CornerCasesTestCase(unittest.TestCase):
    def test_no_renderers(self):
        self.assertEquals(vlogging.renderers, [])
