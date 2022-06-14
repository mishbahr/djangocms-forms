# -*- coding: utf-8 -*-
from django.urls import path

from .views import FormSubmission

urlpatterns = [
    path("forms/submit/", FormSubmission.as_view(), name="djangocms_forms_submissions"),
]
