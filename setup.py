from setuptools import setup
from vlogging import __version__

setup(
    name='visual-logging',
    version=__version__,
    url='https://github.com/dchaplinsky/visual-logging',
    license='MIT',
    author='Dmitry Chaplinsky',
    author_email='chaplinsky.dmitry@gmail.com',
    packages=["vlogging"],
    description="A simple way to generate beautiful html "
                "logs with embedded images for CV purposes.",
    platforms='any'
)
