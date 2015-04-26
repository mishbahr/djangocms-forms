from django.conf.urls import patterns, url

from .views import FormSubmission

urlpatterns = patterns(
    '',
    url(r'^forms/submit/$', FormSubmission.as_view(), name='djangocms_forms_submissions'),
)
