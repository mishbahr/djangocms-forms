=============================
djangocms-forms
=============================

.. image:: http://img.shields.io/travis/mishbahr/djangocms-forms.svg?style=flat-square
    :target: https://travis-ci.org/mishbahr/djangocms-forms/

.. image:: http://img.shields.io/pypi/v/djangocms-forms.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-forms/
    :alt: Latest Version

.. image:: http://img.shields.io/pypi/dm/djangocms-forms.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-forms/
    :alt: Downloads

.. image:: http://img.shields.io/pypi/l/djangocms-forms.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-forms/
    :alt: License

.. image:: http://img.shields.io/coveralls/mishbahr/djangocms-forms.svg?style=flat-square
  :target: https://coveralls.io/r/mishbahr/djangocms-forms?branch=master

This project requires django-cms v3.0 or higher to be properly installed and configured.


Quickstart
----------

1. Install ``djangocms-forms``::

    pip install djangocms-forms

2. Add ``djangocms_forms`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'djangocms_forms',
        ...
    )

3. Set up the database tables (requires south>=1.0.1 if you are using Django 1.6.x)::

    python manage.py migrate

4. Add ``djangocms_forms.urls`` to your project's ``urls`` module::

    urlpatterns = patterns(
        ...
        url(r'^', include('djangocms_forms.urls')),
        ...
    )




Preview
--------

.. image:: http://mishbahr.github.io/djangocms-forms/assets/resized/djangocms_forms_001.jpeg
  :target: http://mishbahr.github.io/djangocms-forms/assets/djangocms_forms_001.png
  :width: 768px
  :align: center

.. image:: http://mishbahr.github.io/djangocms-forms/assets/resized/djangocms_forms_005.jpeg
  :target: http://mishbahr.github.io/djangocms-forms/assets/djangocms_forms_005.png
  :width: 768px
  :align: center

.. image:: http://mishbahr.github.io/djangocms-forms/assets/resized/djangocms_forms_002.jpeg
  :target: http://mishbahr.github.io/djangocms-forms/assets/djangocms_forms_002.png
  :width: 768px
  :align: center

.. image:: http://mishbahr.github.io/djangocms-forms/assets/resized/djangocms_forms_003.jpeg
  :target: http://mishbahr.github.io/djangocms-forms/assets/djangocms_forms_003.png
  :width: 768px
  :align: center

.. image:: http://mishbahr.github.io/djangocms-forms/assets/resized/djangocms_forms_004.jpeg
  :target: http://mishbahr.github.io/djangocms-forms/assets/djangocms_forms_004.png
  :width: 768px
  :align: center

