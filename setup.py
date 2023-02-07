##############################################################################
#
# Copyright (c) 2007-2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup
"""
import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


TESTS_REQUIRE = [
    'zope.browserpage',
    'zope.container',
    'zope.contentprovider',
    'zope.component',
    'zope.site',
    'zope.traversing',
    'zope.testing',
    'zope.testrunner',
]

setup(
    name='z3c.menu.ready2go',
    version='2.0',
    author="Stephan Richter, Roger Ineichen and the Zope Community",
    author_email="zope-dev@zope.dev",
    description="A ready to go menu for Zope3",
    long_description=(
        read('README.txt')
        + '\n\n.. contents::\n\n' +
        read('src', 'z3c', 'menu', 'ready2go', 'README.txt')
        + '\n\n' +
        read('src', 'z3c', 'menu', 'ready2go', 'zcml.txt')
        + '\n\n' +
        read('CHANGES.txt')
    ),
    license="ZPL 2.1",
    keywords="zope3 z3c ready 2 go menu",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
    ],
    url='https://github.com/zopefoundation/z3c.menu.ready2go',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['z3c', 'z3c.menu'],
    python_requires='>=3.7',
    extras_require=dict(
        test=TESTS_REQUIRE,
    ),
    install_requires=[
        'setuptools',
        'z3c.template',
        'zope.browserpage',
        'zope.component >= 3.8',
        'zope.configuration',
        'zope.interface',
        'zope.proxy',
        'zope.publisher',
        'zope.schema',
        'zope.security',
        'zope.site',
        'zope.traversing',
        'zope.viewlet',
    ],
    zip_safe=False,
)
