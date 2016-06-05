# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings  # noqa
from django.utils.translation import ugettext_lazy as _

from appconf import AppConf


class DjangoCMSFormsConf(AppConf):
    PLUGIN_MODULE = _('Generic')
    PLUGIN_NAME = _('Form')
    FIELDSETS = None
    FILE_STORAGE_DIR = 'djangocms_forms'
    FILE_STORAGE = settings.DEFAULT_FILE_STORAGE

    ALLOWED_FILE_TYPES = (
        'aac', 'ace', 'ai', 'aiff', 'avi', 'bmp', 'dir', 'doc', 'docx', 'dmg',
        'eps', 'fla', 'flv', 'gif', 'gz', 'hqx', 'ico', 'indd', 'inx', 'jpg',
        'jar', 'jpeg', 'md', 'mov', 'mp3', 'mp4', 'mpc', 'mkv', 'mpg', 'mpeg',
        'ogg', 'odg', 'odf', 'odp', 'ods', 'odt', 'otf', 'pdf', 'png', 'pps',
        'ppsx', 'ps', 'psd', 'rar', 'rm', 'rtf', 'sit', 'swf', 'tar', 'tga',
        'tif', 'tiff', 'ttf', 'txt', 'wav', 'wma', 'wmv', 'xls', 'xlsx', 'xml',
        'zip'
    )
    MAX_UPLOAD_SIZE = 5242880  # 5MB

    FIELD_TYPES = (
        ('text', _('Text')),
        ('textarea', _('Text Area')),
        ('email', _('Email')),
        ('number', _('Number')),
        ('phone', _('Phone')),
        ('url', _('URL')),
        ('checkbox', _('Checkbox')),
        ('checkbox_multiple', _('Multi Checkbox')),
        ('select', _('Drop down')),
        ('radio', _('Radio')),
        ('file', _('File Upload')),
        ('date', _('Date')),
        ('time', _('Time')),
        ('password', _('Password')),
        ('hidden', _('Hidden')),
    )

    DEFAULT_FIELD_TYPE = 'text'

    SPAM_PROTECTIONS = (
        (0, _('None')),
        (1, _('Honeypot')),
        (2, _('ReCAPTCHA')),
    )

    DEFAULT_SPAM_PROTECTION = 0

    RECAPTCHA_PUBLIC_KEY = ''
    RECAPTCHA_SECRET_KEY = ''

    TEMPLATES = (
        ('djangocms_forms/form_template/default.html', _('Default')),
    )

    DEFAULT_TEMPLATE = 'djangocms_forms/form_template/default.html'

    DATETIME_FORMAT = '%d/%m/%Y %H:%M'
    EXPORT_FILENAME = 'export-{form_name}-%Y-%m-%d'

    HASHIDS_SALT = settings.SECRET_KEY

    USE_HTML5_REQUIRED = False

    WIDGET_CSS_CLASSES = {}

    ALLOW_CUSTOM_FIELD_NAME = True

    class Meta:
        prefix = 'djangocms_forms'
