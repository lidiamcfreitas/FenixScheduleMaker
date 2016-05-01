# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='scheduleMaker',
    version='0.0.1',
    description='Helper app for making schedules using FenixEdu',
    long_description=readme,
    author='Lídia Freitas',
    author_email='lidiamcfreitas@gmail.com',
    url='https://github.com/lidiamcfreitas/FenixScheduleMaker',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

