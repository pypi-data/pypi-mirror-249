from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.10'
DESCRIPTION = 'IpPersian'
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="IpPersian",
    version=VERSION,
    author="Erfan Mahigir (Sarzamin Danesh Pishro)",
    author_email="<info@Lssc.ir>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'Date', 'Persian', 'Time',
              'Gregorian', 'Convert', 'Iranian'],

    classifiers=[
        "Framework :: Django",
        "Framework :: Flask",
        "Framework :: FastAPI",
        "Framework :: IDLE",
        "Framework :: IPython",
        "Framework :: Jupyter",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Android",
        "Operating System :: iOS",
        "License :: OSI Approved :: MIT License"
    ]
)
