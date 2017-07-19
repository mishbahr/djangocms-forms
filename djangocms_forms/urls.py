# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import FormSubmission

urlpatterns = [
    url(r'^forms/submit/$', csrf_exempt( FormSubmission.as_view()), name='djangocms_forms_submissions'),
]
