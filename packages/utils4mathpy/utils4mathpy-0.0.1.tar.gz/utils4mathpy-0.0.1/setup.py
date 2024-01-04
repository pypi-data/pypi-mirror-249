from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Math tools package for python'
# LONG_DESCRIPTION = 'A package that provides a set of math tools for your python projects'

# Setting up
setup(
    name = "utils4mathpy",
    version = VERSION,
    author = "ManelRosPuig (Manel Ros Puig)",
    author_email = "<manel.rospuig@gmail.com>",
    description = DESCRIPTION,
    long_description_content_type = "text/markdown",
    packages = find_packages(),
    install_requires = [],
    keywords = ['python', 'math', 'tools', 'numbers', 'prime numbers', 'py-math', 'divisors', 'factorize'],
    classifiers = []
)