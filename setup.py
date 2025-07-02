#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from os import path
from codecs import open

here = path.abspath(path.dirname(__file__))

# get the dependencies and installs

with open(
    path.join(here, "requirements.txt"), encoding="utf-8"
) as f:
    all_reqs = f.read().split("\n")

install_requires = [
    x.strip() for x in all_reqs if "git+" not in x
]

requirements = ["requests"]

test_requirements = [ ]

setup(
    author="T. Moudiki",
    author_email='thierry.moudiki@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Tools for interacting with Techtonique API",
    install_requires=install_requires,
    license="MIT license",
    long_description='High level Python functions for interacting with Techtonique APIs',
    include_package_data=True,
    keywords=['Techtonique', 'api'],
    name='techtonique_apis',
    packages=find_packages(),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Techtonique/techtonique-apis',
    version='0.8.2',
    zip_safe=False,
)
