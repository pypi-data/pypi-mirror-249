##############################################################################
#
# Copyright (c) 2019-2023 Jens Vagelpohl and Contributors.
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
import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(
    name='dataflake.wsgi.werkzeug',
    version='2.1',
    url='https://github.com/dataflake/dataflake.wsgi.werkzeug',
    project_urls={
        'Documentation': 'https://dataflakewsgiwerkzeug.readthedocs.io',
        'Issue Tracker': ('https://github.com/dataflake/'
                          'dataflake.wsgi.werkzeug/issues'),
        'Sources': 'https://github.com/dataflake/dataflake.wsgi.werkzeug',
    },
    license='ZPL 2.1',
    description='PasteDeploy entry point for the werkzeug WSGI server',
    author='Jens Vagelpohl and Contributors',
    author_email='jens@dataflake.org',
    long_description=(read('README.rst') + '\n\n' + read('CHANGES.rst')),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['dataflake', 'dataflake.wsgi'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Zope',
        'Framework :: Zope :: 5',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
    python_requires='>=3.7',
    install_requires=[
        'setuptools',
        'werkzeug',
        'Zope >= 5',  # To avoid reinventing the skeleton creation
    ],
    extras_require={
        'docs': [
            'Sphinx',
            'sphinx_rtd_theme',
            'pkginfo',
        ],
    },
    entry_points={
        'paste.server_runner': [
            'main=dataflake.wsgi.werkzeug:serve_paste',
            'debugger=dataflake.wsgi.werkzeug:serve_debugger',
        ],
        'console_scripts': [
            'mkwerkzeuginstance=dataflake.wsgi.werkzeug.configurator:mkzope',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
