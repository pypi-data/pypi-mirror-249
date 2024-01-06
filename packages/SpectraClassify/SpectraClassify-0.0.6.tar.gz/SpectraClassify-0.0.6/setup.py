from setuptools import setup, find_packages
import subprocess

with open("README.md", "r") as fh:
    desc = fh.read()

__version__ = "0.0.6"

REPO_NAME = "SpectraClassify"
AUTHOOR_NAME = "Sadhin"
SRC_REPO = "spectraclassify"
AUTHOR_EMAIL = "sadhin.aiub.cse@gmail.com"


setup(
    name=REPO_NAME,
    version=__version__,
    author=AUTHOOR_NAME,
    author_email=AUTHOR_EMAIL,
    description="SpectraClassify is a python package for zero code image classification within the browser",
    long_description=desc,
    long_description_content_type="text/markdown",
    url=f"https://github.com/sadhiin/spectraclassify",
    install_requires=[
        'globals==0.3.36',
        'numpy==1.24.3',
        'opencv-python==4.8.1.78',
        'tensorflow==2.13',
        'pillow==10.2.0',
        'Flask==3.0.0',
        'Flask-Cors==4.0.0',
        'python-box==7.1.1',
        'ensure==1.0.4'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        "console_scripts": [
            "run = spectraclassify.main:runnapplication",
        ]},
)
