from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'Stock information analysis package'
LONG_DESCRIPTION = 'A package for loading historical stock data, calculating SMA and RSI, and writing results to CSV files.'

# Setting up
setup(
    name="stockinfoain1001",
    version=VERSION,
    author="Abdurrahman Javat",  # Update with your name
    author_email="<abdurrahman.javat@bahcesehir.edu.tr>",  # Update with your email
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'stock', 'finance', 'SMA', 'RSI'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
