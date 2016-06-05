# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from cms.models.fields import PageField
from jsonfield import JSONField
from unidecode import unidecode

from .conf import settings
from .fields import PluginReferenceField
from .managers import ActiveFormManager


@python_2_unicode_compatible
class Form(models.Model):
    name = models.CharField(_('Name'), max_length=255, db_index=True, editable=False)

    objects = models.Manager()
    active_objects = ActiveFormManager()

    class Meta:
        verbose_name = _('form')
        verbose_name_plural = _('forms')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class FormDefinition(CMSPlugin):
    name = models.CharField(_('Form Name'), max_length=255)

    title = models.CharField(_('Title'), max_length=150, blank=True)
    description = models.TextField(_('Description'), blank=True)
    submit_btn_txt = models.CharField(
        _('Submit Button Text'), max_length=100, default=_('Submit'),
        help_text=_('Text for the Submit Button. The default is \'Submit\''))

    post_submit_msg = models.TextField(
        _('Post Submit Message'), blank=True, default=_('Thank You'),
        help_text=_('Display this message to users after they submit your form.'))

    # 'HTTP redirect after successful submission'
    success_redirect = models.BooleanField(
        _('Redirect?'), default=False,
        help_text=_('HTTP redirect after successful submission'))
    page_redirect = PageField(
        verbose_name=_('Page URL'), blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text=_('A page has priority over an external URL'))
    external_redirect = models.URLField(
        _('External URL'), blank=True,
        help_text=_('e.g. http://example.com/thank-you'))
    redirect_delay = models.PositiveIntegerField(
        _('Redirect Delay'), blank=True, null=True,
        help_text=_('Wait this number of milliseconds before redirecting. '
                    '1000 milliseconds = 1 second.')
    )

    # Email
    email_to = models.CharField(
        _('Send form data to e-mail address'), max_length=255, blank=True,
        help_text=_('Separate several addresses with a comma.'))
    email_from = models.EmailField(_('Sender Email Address'), max_length=255, blank=True)
    email_subject = models.CharField(_('Email Subject'), max_length=255, blank=True)
    email_uploaded_files = models.BooleanField(
        _('Send uploaded files as email attachments'), default=True)

    # Save to database
    save_data = models.BooleanField(
        _('Save to database'),  default=True,
        help_text=_('Logs all form submissions to the database.'))
    spam_protection = models.SmallIntegerField(
        _('Spam Protection'),
        choices=settings.DJANGOCMS_FORMS_SPAM_PROTECTIONS,
        default=settings.DJANGOCMS_FORMS_DEFAULT_SPAM_PROTECTION)

    form_template = models.CharField(
        _('Form Template'), max_length=150, blank=True,
        choices=settings.DJANGOCMS_FORMS_TEMPLATES,
        default=settings.DJANGOCMS_FORMS_DEFAULT_TEMPLATE,
    )

    plugin_reference = PluginReferenceField(Form, related_name='plugin')

    class Meta:
        verbose_name_plural = _('forms')
        verbose_name = _('form')

    def __str__(self):
        return self.name

    @property
    def redirect_url(self):
        if self.page_redirect:
            return self.page_redirect.get_absolute_url()
        elif self.external_redirect:
            return self.external_redirect

    @property
    def upload_to(self):
        return '%s-%s' % (
            slugify(unidecode(self.name)).replace('_', '-'),
            self.plugin_reference_id)

    @property
    def use_honeypot(self):
        return self.spam_protection == 1

    @property
    def use_recaptcha(self):
        return self.spam_protection == 2

    def copy_relations(self, oldinstance):
        for field in oldinstance.fields.all():
            field.pk = None
            field.form = self
            field.save()


@python_2_unicode_compatible
class FormField(models.Model):
    form = models.ForeignKey(FormDefinition, related_name='fields')
    field_type = models.CharField(
        _('Field Type'), max_length=100,
        choices=settings.DJANGOCMS_FORMS_FIELD_TYPES,
        default=settings.DJANGOCMS_FORMS_DEFAULT_FIELD_TYPE)
    label = models.CharField(_('name'), max_length=255)
    field_name = models.CharField(_('Custom Field Name'), max_length=255, blank=True)
    placeholder_text = models.CharField(_('Placeholder Text'), blank=True, max_length=100)
    required = models.BooleanField(_('Required'), default=True)
    help_text = models.TextField(
        _('Description'), blank=True,
        help_text=_('A description / instructions for this field.'))
    initial = models.CharField(_('Default Value'), max_length=255, blank=True)
    choice_values = models.TextField(
        _('Choices'),  blank=True,
        help_text=_('Enter options one per line. For "File Upload" '
                    'field type, enter allowed filetype (e.g .pdf) one per line.'))
    position = models.PositiveIntegerField(_('Position'), blank=True, null=True)

    class Meta:
        verbose_name_plural = _('fields')
        verbose_name = _('field')
        ordering = ('position', )

    def __str__(self):
        return self.label

    def build_field_attrs(self, extra_attrs=None):
        """Helper function for building an attribute dictionary for form field."""
        attrs = {}
        if extra_attrs:
            attrs.update(extra_attrs)

        attrs = {
            'required': self.required,
            'label': self.label if self.label else '',
            'initial': self.initial if self.initial else None,
            'help_text': self.help_text,
        }
        return attrs

    def build_widget_attrs(self, extra_attrs=None):
        """Helper function for building an attribute dictionary for form widget."""
        attrs = {}
        if extra_attrs:
            attrs.update(extra_attrs)

        if (self.required and settings.DJANGOCMS_FORMS_USE_HTML5_REQUIRED
                and 'required' not in attrs and self.field_type not in ('hidden', 'radio', )):
            attrs['required'] = 'required'

        css_classes = {
            '__all__': (),
            'text': ('textinput',),
            'textarea': ('textarea', ),
            'email': ('emailinput', ),
            'number': ('integerfield', ),
            'phone': ('telephoneinput', ),
            'url': ('urlfield', ),
            'checkbox': ('booleanfield',),
            'checkbox_multiple': ('checkboxselectmultiple', ),
            'select': ('choicefield', ),
            'radio': ('radioselect', ),
            'file': ('filefield', ),
            'date': ('dateinput', ),
            'time': ('timeinput', ),
            'password': ('passwordinput', ),
            'hidden': ('hiddeninput', ),
        }

        css_classes.update(settings.DJANGOCMS_FORMS_WIDGET_CSS_CLASSES)

        css_classes = (attrs.get('class', ''), ) + \
            css_classes.get('__all__', ()) + \
            css_classes.get(self.field_type, ())

        attrs['class'] = ' '.join(cls.strip() for cls in css_classes if cls.strip())
        return attrs

    def get_choices(self):
        if self.choice_values:
            regex = re.compile('[\s]*\n[\s]*')
            choices = regex.split(self.choice_values)
            return [(choice, choice) for choice in choices]


@python_2_unicode_compatible
class FormSubmission(models.Model):
    plugin = models.ForeignKey(
        Form, verbose_name=_('Form'), editable=False, related_name='submissions')
    creation_date = models.DateTimeField(_('Date'), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('User'), editable=False, null=True)
    ip = models.GenericIPAddressField(verbose_name='IP', blank=True, null=True)
    referrer = models.CharField(_('Referrer URL'), max_length=150, blank=True)

    form_data = JSONField(_('Form Data'))

    class Meta:
        verbose_name_plural = _('form submissions')
        verbose_name = _('form submission')
        ordering = ('-creation_date', )
        permissions = (
            ('export_formsubmission', 'Can export Form Submission'),
        )

    def __str__(self):
        return u'%s' % self.plugin
