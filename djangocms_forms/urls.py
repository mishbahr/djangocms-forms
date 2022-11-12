# -*- coding: utf-8 -*-

from .views import FormSubmission

# This is ugly, but I gather there are still people running outdated Django versions.

try:
    from django.conf.urls import url
except ImportError:
    from django.urls import path

    urlpatterns = [
        path("forms/submit/", FormSubmission.as_view(), name="djangocms_forms_submissions"),
    ]

else:
    urlpatterns = [
        url(r"^forms/submit/$", FormSubmission.as_view(), name="djangocms_forms_submissions"),
    ]
