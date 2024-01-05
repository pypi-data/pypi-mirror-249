#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 17:51:50 2023

@author: javiera.quiroz
"""

from setuptools import setup

setup(
    name='FlyBaseDownloads',
    version='1.0.8.2',
    license='MIT',
    author='Javiera Quiroz Olave',
    url= 'https://github.com/JavieraQuirozO/FlyBaseDownloads',
    author_email='javiera.quiroz@biomedica.udec.cl',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=open('requirements.txt').readlines(),
    description='Wrapped to download Flybase data with Python, easily and quickly.',
    packages=['FlyBaseDownloads', 'FlyBaseDownloads.classes', 'FlyBaseDownloads.downloads', 'FlyBaseDownloads.utilities'],
    package_data={
        'FlyBaseDownloads': ['serviceAccountKey.json'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
