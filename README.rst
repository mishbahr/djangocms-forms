================
djangocms-forms
================

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

This package is compatible with `Aldryn <http://www.aldryn.com/en/marketplace/djangocms-forms/>`_.


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

3. Sync database tables (requires south>=1.0.1 if you are using Django 1.6.x)::

    python manage.py migrate

4. Add ``djangocms_forms.urls`` to your project's ``urls`` module or create a django CMS page to hook the application into. In ``Advanced Settings``, set its Application to ``Forms`` (this requires a server restart)::

    urlpatterns = patterns(
        ...
        url(r'^', include('djangocms_forms.urls')),
        ...
    )

5. To use reCAPTCHA for spam protection, you need to sign up for an API key pair for your site::

    DJANGOCMS_FORMS_RECAPTCHA_PUBLIC_KEY = '<recaptcha_site_key>'
    DJANGOCMS_FORMS_RECAPTCHA_SECRET_KEY = '<recaptcha_secret_key>'

You can register a new site via https://www.google.com/recaptcha/admin



Configuration
--------------

Plugin(s) Module - If module is None, plugin is grouped Generic group::

    DJANGOCMS_FORMS_PLUGIN_MODULE = _('Generic')

Name of the plugin::

    DJANGOCMS_FORMS_PLUGIN_NAME = _('Form')

The path to the default template used to render the template::

   DJANGOCMS_FORMS_DEFAULT_TEMPLATE = 'djangocms_forms/form_template/default.html'

or override the ``Form Template`` dropdown choices to have different template options::

    DJANGOCMS_FORMS_TEMPLATES = (
        ('djangocms_forms/form_template/default.html', _('Default')),
    )

HTML5 required - When set to True all required fields inputs will be rendered with HTML5 ``required=required`` attribute::

    DJANGOCMS_FORMS_USE_HTML5_REQUIRED = False


By default, ``djangocms-forms`` adds additional css classes to all form inputs. e.g. a ``Text`` field generates an ``<input class="textinput">`` You can override this to integrate your own CSS framework::

    DJANGOCMS_FORMS_WIDGET_CSS_CLASSES = {'__all__': ('form-control', ) }

e.g. the above setting would generate ``<input class"form-control" ....`` for all fields.

By default, djangocms-forms will redirect a successful form submission after 1000 milliseconds (1 second). You may provide your own redirect delay value for all forms site-wide via settings::

    DJANGOCMS_FORMS_REDIRECT_DELAY = 10000  # 10 seconds

or on a per-form basis via the ``redirect_delay`` field. The order of precedence for the redirect value is always::

    instance.redirect_delay > DJANGOCMS_FORMS_REDIRECT_DELAY > 1000 (default)


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


You may also like...
--------------------

* djangocms-disqus - https://github.com/mishbahr/djangocms-disqus
* djangocms-embed - https://github.com/mishbahr/djangocms-embed
* djangocms-fbcomments - https://github.com/mishbahr/djangocms-fbcomments
* djangocms-gmaps - https://github.com/mishbahr/djangocms-gmaps
* djangocms-instagram - https://github.com/mishbahr/djangocms-instagram
* djangocms-responsive-wrapper - https://github.com/mishbahr/djangocms-responsive-wrapper
* djangocms-twitter2 - https://github.com/mishbahr/djangocms-twitter2
* djangocms-youtube - https://github.com/mishbahr/djangocms-youtube
