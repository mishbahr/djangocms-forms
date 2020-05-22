



from django.conf.urls import url

from .views import FormSubmission

urlpatterns = [
    url(r'^forms/submit/$', FormSubmission.as_view(), name='djangocms_forms_submissions'),
]
