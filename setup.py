from distutils.core import setup
from setuptools import find_packages

setup(
    name='pysqes',
    version='0.1',
    description='A simple queue service using Amazon SQS and boto',
    long_description=open('README.md').read(),
    author='Essau Ramirez',
    author_email='saumotions+pypi@gmail.com',
    license='Apache',
    keywords=('queue', 'amazon', 'distributed'),
    packages=find_packages(exclude=['tests', ]),
    install_requires=[
        item for item in
        open("requirements.txt").read().split("\n")
    ]
)
