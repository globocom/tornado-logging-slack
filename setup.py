# -*- coding:utf-8 -*-

from setuptools import find_packages, setup

version = '0.1.0'

setup(
    name='tornado-logging-slack',
    version=version,
    description='Log tornado in slack chat without block eventloop',
    long_description='',
    classifiers=[],
    keywords='tornado slack logging',
    author='Globo.com',
    author_email='backstage1@corp.globo.com',
    url='https://github.com/globocom/tornado-logging-slack',
    license='MIT',
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests.*"]),
    platforms=['any'],
    install_requires=[
        'tornado',
        'slacker-log-handler'
    ],
    extras_require={
        'tests': [
            'nose',
            'flake8',
        ]
    }
)
