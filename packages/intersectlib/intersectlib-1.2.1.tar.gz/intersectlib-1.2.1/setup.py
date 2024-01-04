from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'find intersections and remainders.'
LONG_DESCRIPTION = 'A package to find intersections and remainders between two ranges.'

# Setting up
setup(
    name="intersectlib",
    version=VERSION,
    author="Ricardo Ducker",
    author_email="<duckerricardo@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'ranges', 'intersections', 'destinations', 'remainders'],
    classifiers=[
        "Development Status :: 2 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)