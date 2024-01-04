#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages

import fsm_admin

readme = open("README.rst").read()

setup(
    name="django-fsm-admin-maintained",
    version=fsm_admin.__version__,
    author=fsm_admin.__author__,
    description="Integrate django-fsm state transitions into the django admin with django 4 support.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    author_email="barbaros@bidnamic.com",
    url="https://github.com/7tg/django-fsm-admin-maintained",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=1.6",
        "django-fsm>=2.1.0",
    ],
    keywords="django fsm admin",
    license="MIT",
    platforms=["any"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.11",
    ]
)
