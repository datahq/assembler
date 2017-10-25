# -*- coding: utf-8 -*-

import os
import io
from setuptools import setup, find_packages


# Helpers
def read(*paths):
    """Read a text file."""
    basedir = os.path.dirname(__file__)
    fullpath = os.path.join(basedir, *paths)
    contents = io.open(fullpath, encoding='utf-8').read().strip()
    return contents


# Prepare
PACKAGE = 'datapackage_pipelines_assembler'
NAME = PACKAGE.replace('_', '-')
INSTALL_REQUIRES = [
    'datapackage-pipelines',
    'datapackage-pipelines-elasticsearch>=0.0.3',
    'datapackage-pipelines-aws>=0.0.9',
    'psycopg2',
    'tweepy',
    'facebook-sdk',
    'google-api-python-client==1.5.3',
]
TESTS_REQUIRE = [
    'pylama',
    'tox',
    'moto',
    'boto3'
]
README = read('README.md')
VERSION = read(PACKAGE, 'VERSION')
PACKAGES = find_packages(exclude=['examples', 'tests'])


# Run
setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require={'develop': TESTS_REQUIRE},
    zip_safe=False,
    long_description=README,
    description='{{ DESCRIPTION }}',
    author='DataHQ',
    url='https://github.com/datahq/assembler',
    license='MIT',
    keywords=[
        'data',
        'analytics'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        'console_scripts': [
            'assembler-dpp = datapackage_pipelines_assembler.cli:main'
        ]
    }
)
