from distutils.core import setup
from setuptools import find_packages

entry_points = {}
console_scripts = entry_points['console_scripts'] = [
    'pysqes = pysqes.bin.pysqes:main'
]

setup(
    name='pysqes',
    version='0.2.1',
    license='Apache',
    description='A simple queue service using Amazon SQS and boto',
    long_description=open('README.rst').read(),
    author='Essau Ramirez',
    author_email='saumotions+pypi@gmail.com',
    url='https://github.com/sauramirez/pysqes',
    download_url='https://github.com/sauramirez/pysqes',
    keywords=('queue', 'amazon', 'distributed'),
    packages=find_packages(exclude=['tests', ]),
    include_package_data = True,
    entry_points=entry_points,
    install_requires=[
        item for item in
        open("requirements.txt").read().split("\n")
    ]
)
