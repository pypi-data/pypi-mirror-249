#!/usr/bin/env python
# encoding: utf-8
# vim:sts=4:sw=4
"""Helps building and automatizing building LibreOffice AppImages."""

from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="loaih",
    version="1.3.3",
    description="LOAIH - LibreOffice AppImage Helpers, help build a LibreOffice AppImage",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Emiliano Vavassori",
    author_email="syntaxerrormmm@libreoffice.org",
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'loaih = loaih.script:cli',
        ],
    },
    install_requires=['click', 'lxml', 'packaging', 'pyyaml', 'requests'],
    license='MIT',
    url='https://git.libreitalia.org/LibreItalia/loaih/',
)
