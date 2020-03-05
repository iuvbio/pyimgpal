
from setuptools import setup


__version__ = '0.0.1'

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    dependencies = [d.strip() for d in f.readlines() if not d.startswith('#')]

setup(
    name='pyimgpal',
    version=__version__,
    url='',
    license='',
    author='iuvbio',
    author_email='cryptodemigod@protonmail.com',
    description='A simple script to create a 16 colour scheme from an image.',
    long_description=long_description,
    install_requires=dependencies,
    py_modules=['imgpal'],
    entry_points={
        'console_scripts': 'imgpal=imgpal:main'
    },
)
