# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.db import models
from django.template.loader import select_template
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .conf import settings
from .forms import FormBuilder, FormDefinitionAdminForm, FormFieldInlineForm
from .models import FormDefinition, FormField


class FormFieldInline(admin.StackedInline):
    model = FormField
    form = FormFieldInlineForm
    extra = 0

    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(
                attrs={'rows': 4, 'cols': 50})
        },
    }

    def get_fieldsets(self, request, obj=None):
        fields = (
            ('label', 'field_type', 'required'),
            'initial', 'placeholder_text', 'help_text', 
            'choice_values', 'position', 
        )

        if settings.DJANGOCMS_FORMS_ALLOW_CUSTOM_FIELD_NAME:
            fields = fields + ('field_name', )

        fieldsets = (
            (None, {
                'fields': fields
            }),
        )
        return fieldsets

    class Media:
        css = {
            'all': ('css/djangocms_forms/admin/djangocms_forms.css',)
        }
        js = (
            'js/djangocms_forms/libs/jquery.min.js',
            'js/djangocms_forms/libs/jquery-ui.min.js',

            'js/djangocms_forms/admin/jquery-inline-positioning.js',
            'js/djangocms_forms/admin/jquery-inline-rename.js',
            'js/djangocms_forms/admin/jquery-inline-collapsible.js',
            'js/djangocms_forms/admin/jquery-inline-toggle-fields.js',
        )


class FormPlugin(CMSPluginBase):
    name = settings.DJANGOCMS_FORMS_PLUGIN_NAME
    module = settings.DJANGOCMS_FORMS_PLUGIN_MODULE
    model = FormDefinition
    cache = False
    form = FormDefinitionAdminForm
    inlines = (FormFieldInline, )
    render_template = settings.DJANGOCMS_FORMS_DEFAULT_TEMPLATE

    def get_fieldsets(self, request, obj=None):
        if settings.DJANGOCMS_FORMS_FIELDSETS:
            return settings.DJANGOCMS_FORMS_FIELDSETS

        fieldsets = (
            (None, {'fields': ('name', )}),

            (None, {
                'description': _('The <strong>Title</strong> and <strong>Description</strong> '
                                 'will display above the input fields and Submit button.'),
                'fields': ('title', 'description', )
            }),
            (None, {
                'description': _('By default, the Submit Button will say <strong>Submit</strong>. '
                                 'You can change this to say whatever you want'),
                'fields': ('submit_btn_txt', 'form_template', )
            }),
            (None, {
                'description': _('You can also change the message that appears after someone '
                                 'submits your form. '
                                 'By default, this says <strong>Thank you!</strong>, '
                                 'but you are welcome to change this text as well.'),
                'fields': ('post_submit_msg', )
            }),
            (None, {
                'fields': ('success_redirect', ('page_redirect', 'external_redirect'), 'redirect_delay',),
            }),
            (None, {
                'description': '<strong>Submission Settings</strong> &mdash; '
                               'Choose storage options to capture form data. You can enter '
                               'an email address to have the form submissions emailed to you or '
                               'log all the form submissions to the database.',
                'fields': ('email_to', 'email_from', 'email_subject',
                           'email_uploaded_files', 'save_data', 'spam_protection', ),
            }),
        )
        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        # returns the first template that exists, falling back to bundled template
        return select_template([
            instance.form_template,
            settings.DJANGOCMS_FORMS_DEFAULT_TEMPLATE,
            'djangocms_forms/form_template/default.html'
        ])

    def render(self, context, instance, placeholder):
        context = super(FormPlugin, self).render(context, instance, placeholder)
        request = context['request']

        form = FormBuilder(
            initial={'referrer': request.path_info}, form_definition=instance,
            label_suffix='', auto_id='%s')

        redirect_delay = instance.redirect_delay or \
            getattr(settings, 'DJANGOCMS_FORMS_REDIRECT_DELAY', 1000)

        context.update({
            'form': form,
            'recaptcha_site_key': settings.DJANGOCMS_FORMS_RECAPTCHA_PUBLIC_KEY,
            'redirect_delay': redirect_delay
        })
        return context


plugin_pool.register_plugin(FormPlugin)
