import sys
import unittest
from pathlib import Path

DUMMIES = str(Path(__file__).parent / "dummies")
BLOCKED = ("vlogging", "cv2", "numpy", "PIL", "matplotlib", "pylab")


class CornerCasesTestCase(unittest.TestCase):
    def test_no_renderers(self):
        # Reimport vlogging with dummy cv2/PIL/matplotlib modules that raise
        # ImportError, then restore the real modules for the other tests
        saved = {name: mod for name, mod in sys.modules.items()
                 if name.split(".")[0] in BLOCKED}

        sys.path.insert(0, DUMMIES)
        try:
            for name in saved:
                del sys.modules[name]

            import vlogging
            self.assertEqual(vlogging.renderers, [])
        finally:
            sys.path.remove(DUMMIES)
            for name in [name for name in sys.modules
                         if name.split(".")[0] in BLOCKED]:
                del sys.modules[name]
            sys.modules.update(saved)
