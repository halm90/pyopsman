#!/usr/bin/env python
"""
      Copyright 2019, Hal Moroff
      Licensed under the GNU General Purpose License.
"""

from setuptools import setup, find_packages

base_url = 'https://github.com/halm90/pyopsman'
version_tag = '0.0.1'

setup(
    name='pyopsman',
    version=version_tag,
    description='Non-official Opsman REST Admin API library',
    author='Hal Moroff',
    license='Apache License Version 2.0',
    author_email='halm91@gmail.com',
    url=base_url,
    download_url=base_url + '/archive/' + version_tag + '.tar.gz',
    packages=find_packages(),
    keywords=['opsman', 'rest-client'],
    platforms=['Any']
)
