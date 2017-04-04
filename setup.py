import os
import sys
from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Tool to convert ODK-style XLSForms into Django models and HTML templates for use with wq (https://wq.io/)
"""


def parse_markdown_readme():
    """
    Convert README.md to RST via pandoc, and load into memory
    (fallback to LONG_DESCRIPTION on failure)
    """
    # Attempt to run pandoc on markdown file
    import subprocess
    try:
        subprocess.call(
            ['pandoc', '-t', 'rst', '-o', 'README.rst', 'README.md']
        )
    except OSError:
        return LONG_DESCRIPTION

    # Attempt to load output
    try:
        readme = open(os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        ))
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()


setup(
    name='xlsconv',
    version='1.0.0-dev',
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='https://github.com/wq/xlsform-converter',
    license='MIT',
    packages=['xlsconv'],
    package_data={
        'xlsconv': [
            'templates/*.*',
            'templates/fields/*.*',
        ],
    },
    description=LONG_DESCRIPTION.strip(),
    long_description=parse_markdown_readme(),
    install_requires=[
        'pystache',
        'pyxform',
    ],
    entry_points='''
        [console_scripts]
        xls2html=xlsconv.html:main
        xls2django=xlsconv.django:main
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    test_suite='tests',
)
