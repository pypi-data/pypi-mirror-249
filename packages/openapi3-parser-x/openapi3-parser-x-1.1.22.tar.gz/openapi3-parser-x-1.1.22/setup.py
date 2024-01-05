#!/usr/bin/env python

from setuptools import find_packages, setup

# from src import openapi_parser

setup(
    name='openapi3-parser-x',
    author='MrAdhit',
    author_email='mradhit@kingland.id',
    url="https://github.com/MrAdhit/openapi3-parser",
    project_urls={
        "Source": "https://github.com/MrAdhit/openapi3-parser",
    },
    version='1.1.22',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={"openapi_parser": ["py.typed"]},
    license="MIT",
    description='OpenAPI v3 parser',
    keywords="swagger, python, swagger-parser, openapi3-parser-x, parser, openapi3, swagger-api",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
    ],
    setup_requires=[
        "prance>=0.20.2",
    ],
    install_requires=[
        "prance>=0.20.2",
        "openapi-spec-validator==0.6.0",
    ],
)
