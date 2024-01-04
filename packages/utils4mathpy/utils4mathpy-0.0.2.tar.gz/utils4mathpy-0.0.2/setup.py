from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Math tools package for python'

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
    keywords = ['python', 'math', 'tools', 'numbers', 'prime numbers', 'utils4mathpy', 'divisors', 'factorize'],
    classifiers = []
)