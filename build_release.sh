#!/bin/bash
pip install --upgrade setuptools
pip install --upgrade wheel
pip install --upgrade twine
python setup.py sdist bdist_wheel
# Test PyPi
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# Prod PyPi
twine upload dist/*