# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from .forms import FormBuilder
from .models import FormDefinition
from .signals import form_submission
from .uploads import handle_uploaded_files
from .utils import hashid_to_int

try:
    from django.http import JsonResponse
except ImportError:
    from .compat import JsonResponse


class FormSubmission(FormView):
    form_class = FormBuilder
    http_method_names = ['post']

    def get_form_kwargs(self):
        form_kwargs = super(FormSubmission, self).get_form_kwargs()
        form_id = hashid_to_int(self.request.POST.get('form_id'))
        form_definition = get_object_or_404(FormDefinition, pk=form_id)
        form_kwargs.update({
            'form_definition': form_definition
        })
        return form_kwargs

    def form_valid(self, form, *args, **kwargs):
        handle_uploaded_files(form)
        form.save(request=self.request)
        form_submission.send(
            sender=self.__class__,
            form=form.form_definition,
            cleaned_data=form.cleaned_data)

        if self.request.is_ajax():
            response = {
                'formIsValid': True,
                'redirectUrl': form.redirect_url
            }
            return JsonResponse(response)
        else:
            messages.success(self.request, strip_tags(form.form_definition.post_submit_msg))
            return redirect(form.redirect_url or form.cleaned_data['referrer'])

    def form_invalid(self, form, *args, **kwargs):
        if self.request.is_ajax():
            response = {
                'formIsValid': False,
                'errors': form.errors,
            }
            return JsonResponse(response)
        else:
            messages.error(self.request, _(u'Invalid form data, one or more fields had errors'))
            return redirect(form.cleaned_data['referrer'])
