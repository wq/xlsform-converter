import os
import sys
from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Tool to convert ODK-style XLSForms into Django models and HTML templates for use with wq (https://wq.io/)
"""


def readme():
    try:
        readme = open("README.md")
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()


setup(
    name="xlsconv",
    use_scm_version=True,
    author="S. Andrew Sheppard",
    author_email="andrew@wq.io",
    url="https://github.com/wq/xlsform-converter",
    license="MIT",
    packages=["xlsconv"],
    package_data={
        "xlsconv": [
            "templates/*.*",
            "templates/fields/*.*",
        ],
    },
    description=LONG_DESCRIPTION.strip(),
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=[
        "pyxform",
        "astunparse",
        "black",
        "pystache",
    ],
    setup_requires=[
        "setuptools_scm",
    ],
    entry_points="""
        [console_scripts]
        xls2html=xlsconv.html:main
        xls2django=xlsconv.django:main
    """,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Code Generators",
        "Framework :: Django",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
)
