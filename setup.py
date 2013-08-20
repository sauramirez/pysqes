from distutils.core import setup
from setuptools import find_packages

setup(
    name='pysqes',
    version='0.1.2',
    license='Apache',
    description='A simple queue service using Amazon SQS and boto',
    long_description=open('README.md').read(),
    author='Essau Ramirez',
    author_email='saumotions+pypi@gmail.com',
    url='https://github.com/sauramirez/pysqes',
    download_url='https://github.com/sauramirez/pysqes',
    keywords=('queue', 'amazon', 'distributed'),
    packages=find_packages(exclude=['tests', ]),
    include_package_data = True,
    install_requires=[
        item for item in
        open("requirements.txt").read().split("\n")
    ]
)
