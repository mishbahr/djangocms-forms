# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import os

import requests

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import SET_NULL
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .widgets import ReCaptchaWidget

logger = logging.getLogger('djangocms_forms')


class FormBuilderFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop(
            'max_upload_size', settings.DJANGOCMS_FORMS_MAX_UPLOAD_SIZE)
        allowed_file_types = kwargs.pop(
            'allowed_file_types', settings.DJANGOCMS_FORMS_ALLOWED_FILE_TYPES)
        self.allowed_file_types = [i.lstrip('.').lower()
                                   for i in allowed_file_types]

        super(FormBuilderFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        uploaded_file = super(FormBuilderFileField, self).clean(*args, **kwargs)
        if not uploaded_file:
            if self.required:
                raise forms.ValidationError(_('This field is required.'))
            return uploaded_file

        if not os.path.splitext(uploaded_file.name)[1].lstrip('.').lower() in \
                self.allowed_file_types:
            raise forms.ValidationError(
                _('Sorry, this filetype is not allowed. '
                  'Allowed filetype: %s') % ', '.join(self.allowed_file_types))

        if uploaded_file._size > self.max_upload_size:
            params = {
                'max_size': filesizeformat(self.max_upload_size),
                'size': filesizeformat(uploaded_file._size)
            }
            msg = _(
                'Please keep file size under %(max_size)s. Current size is %(size)s.') % params
            raise forms.ValidationError(msg)

        return uploaded_file


class PluginReferenceField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs.update({'null': True})  # always allow Null
        kwargs.update({'editable': False})  # never allow edits in admin
        kwargs.update({'on_delete': SET_NULL})  # never delete plugin
        super(PluginReferenceField, self).__init__(*args, **kwargs)

    def _create(self, model_instance):
        return self.rel.to._default_manager.create(name=model_instance.name)

    def pre_save(self, model_instance, add):
        if not model_instance.pk and add:
            setattr(model_instance, self.name, self._create(model_instance))
        else:
            reference = getattr(model_instance, self.name)
            if not reference:
                setattr(model_instance, self.name, self._create(model_instance))
                reference = getattr(model_instance, self.name)
            if reference.name != model_instance.name:
                reference.name = model_instance.name
                reference.save()
        return super(PluginReferenceField, self).pre_save(model_instance, add)

    def south_field_triple(self):
        """Returns a suitable description of this field for South."""
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = 'django.db.models.fields.related.ForeignKey'
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class MultipleChoiceAutoCompleteField(forms.MultipleChoiceField):

    def validate(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')
        return value


class HoneyPotField(forms.BooleanField):
    widget = forms.CheckboxInput

    def __init__(self, *args, **kwargs):
        super(HoneyPotField, self).__init__(*args, **kwargs)
        self.required = False
        self.label = _('Are you human? (Sorry, we have to ask!)')
        self.help_text = _('Please don\'t check this box if you are a human.')

    def validate(self, value):
        if value:
            raise forms.ValidationError(_('Doh! You are a robot!'))


class ReCaptchaField(forms.CharField):
    widget = ReCaptchaWidget
    default_error_messages = {
        'invalid': _('Error verifying input, please try again.'),
        'recaptcha_error': _('Connection to reCaptcha server failed.'),
    }
    recaptcha_api = 'https://www.google.com/recaptcha/api/siteverify'

    def __init__(self, *args, **kwargs):
        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, values):
        super(ReCaptchaField, self).clean(values[0])
        response_token = values[0]

        try:
            params = {
                'secret': settings.DJANGOCMS_FORMS_RECAPTCHA_SECRET_KEY,
                'response': response_token
            }
            r = requests.post(self.recaptcha_api, params=params, timeout=5)
            r.raise_for_status()
        except requests.RequestException as e:
            logger.exception(e)
            raise ValidationError(self.error_messages['recaptcha_error'])

        data = r.json()

        if bool(data['success']):
            return values[0]
        else:
            if any(code in data.get('error-codes', {})
                   for code in ('missing-input-secret', 'invalid-input-secret', )):
                logger.exception('Invalid reCaptcha secret key.')
                raise ValidationError(self.error_messages['recaptcha_error'])
            else:
                raise ValidationError(self.error_messages['invalid'], code='invalid')
