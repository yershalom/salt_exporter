#!/usr/bin/env python

from setuptools import setup, find_packages

REQUIREMENTS = [
    'prometheus-client==0.0.13',
]

setup(
    name='salt_exporter',
    description='Best salt exporter',
    version='0.1.0',
    author='Shalom Yerushalmy',
    author_email='yershalom@gmail.com',
    packages=find_packages(exclude=['docs']),
    install_requires=['prometheus-client==0.0.13'],
)
