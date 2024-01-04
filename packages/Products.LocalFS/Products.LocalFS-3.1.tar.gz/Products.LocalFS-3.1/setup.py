##############################################################################
#
# Copyright (c) 1999 Jonothan Farr and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os

from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
_boundary = '\n' + ('-' * 60) + '\n\n'


def _read(name):
    with open(os.path.join(here, name)) as fp:
        return fp.read()


setup(name='Products.LocalFS',
      version='3.1',
      license='BSD License',
      description='The Local File System product',
      long_description=_read('README.rst'),
      classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Web Environment',
        'Framework :: Zope',
        'Framework :: Zope :: 5',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        ],
      keywords='web application server zope',
      author='Jonothan Farr and contributors',
      author_email='jfarr@speakeasy.org',
      maintainer='Jens Vagelpohl',
      maintainer_email='jens@dataflake.org',
      url='https://github.com/dataflake/Products.LocalFS',
      project_urls={
          'Documentation': 'https://productslocalfs.readthedocs.io/',
          'Issue Tracker': ('https://github.com/dataflake/'
                            'Products.LocalFS/issues'),
          'Sources': 'https://github.com/dataflake/Products.LocalFS',
      },
      packages=find_packages('src'),
      include_package_data=True,
      namespace_packages=['Products'],
      package_dir={'': 'src'},
      zip_safe=False,
      python_requires='>=3.7',
      install_requires=[
        'setuptools',
        'Zope >= 5',
        'Products.PythonScripts',
        ],
      extras_require={
          'docs': ['Sphinx', 'sphinx_rtd_theme', 'pkginfo'],
        },
      )
