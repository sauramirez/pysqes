from distutils.core import setup
from setuptools import find_packages

setup(
    name='pysques',
    version='0.1dev',
    packages=find_packages(exclude=['tests', ]),
    license='',
    install_requires=[
        item for item in
        open("requirements.txt").read().split("\n")
    ],
    long_description=open('README.md').read()
)
