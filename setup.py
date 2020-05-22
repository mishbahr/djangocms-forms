#!/usr/bin/env python


import os
import sys

import djangocms_forms

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djangocms_forms.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()

setup(
    name='djangocms-forms',
    version=version,
    description="""The easiest and most flexible Django CMS Form builder w/ ReCaptcha v2 support!""",
    long_description=readme,
    author='Mishbah Razzaque',
    author_email='mishbahx@gmail.com',
    url='https://github.com/mishbahr/djangocms-forms',
    packages=[
        'djangocms_forms',
    ],
    include_package_data=True,
    install_requires=[
        'django-appconf',
        'django-ipware',
        'django-recaptcha',
        'jsonfield',
        'unidecode',
        'tablib',
        'hashids',
        'requests',
        'django-cms>=3.0',
    ],
    license="BSD",
    zip_safe=False,
    keywords='djangocms-forms',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
