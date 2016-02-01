# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import FormSubmission

urlpatterns = patterns(
    '',
    url(r'^forms/submit/$', FormSubmission.as_view(), name='djangocms_forms_submissions'),
)
