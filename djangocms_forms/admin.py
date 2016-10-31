# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
from functools import update_wrapper

from django.contrib import admin, messages
from django.contrib.admin.helpers import AdminErrorList, AdminForm
from django.contrib.auth import get_permission_codename
from django.contrib.auth.admin import csrf_protect_m
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.defaultfilters import slugify, yesno
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from tablib import Dataset

from .conf import settings
from .forms import SubmissionExportForm
from .models import Form, FormSubmission

try:
    from django.contrib.admin.options import IS_POPUP_VAR
except ImportError:
    IS_POPUP_VAR = '_popup'

try:
    from django.contrib.admin.utils import unquote
except ImportError:
    from django.contrib.admin.util import unquote


try:
    from django.http import JsonResponse
except ImportError:
    from .compat import JsonResponse


class FormFilter(admin.SimpleListFilter):
    title = _('Forms')
    parameter_name = 'form'

    def lookups(self, request, model_admin):
        forms = Form.active_objects.all()
        for obj in forms:
            yield (
                str(obj.id), u'%s (%s)' % (obj.name, obj.submission_count)
            )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(plugin_id=self.value())


class FormSubmissionAdmin(admin.ModelAdmin):
    change_form_template = 'admin/djangocms_forms/formsubmission/change_form.html'
    change_list_template = 'admin/djangocms_forms/formsubmission/change_list.html'
    export_form_template = 'admin/djangocms_forms/formsubmission/export_form.html'
    list_display = ('plugin', 'creation_date_display', 'created_by', 'ip', 'referrer', )
    list_filter = (FormFilter, )
    readonly_fields = ('creation_date_display', 'created_by', 'plugin', 'ip', 'referrer', )
    date_hierarchy = 'creation_date'
    fieldsets = (
        (None, {
            'fields': ('creation_date_display', 'created_by', 'ip', 'referrer', )
        }),
    )

    class Media:
        js = (
            'js/djangocms_forms/admin/jquery-form-export.js',
        )

    def has_add_permission(self, request):
        return False

    def has_export_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('export', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    def creation_date_display(self, obj):
        return obj.creation_date.strftime(settings.DJANGOCMS_FORMS_DATETIME_FORMAT)
    creation_date_display.short_description = _('Sent On')

    def get_queryset(self, request):
        qs = super(FormSubmissionAdmin, self).get_queryset(request)
        return qs.select_related('created_by', 'plugin', )

    def get_urls(self):
        """
        Add the export view to urls.
        """
        urls = super(FormSubmissionAdmin, self).get_urls()
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        extra_urls = [
            url(r'^export/$', wrap(self.export_view), name='%s_%s_export' % info),
        ]
        return extra_urls + urls

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        context = extra_context or {}
        context.update({
            'title': self.opts.verbose_name_plural.title(),
            'has_export_permission': self.has_export_permission(request),
        })
        return super(FormSubmissionAdmin, self).changelist_view(
            request, extra_context=context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = extra_context or {}
        obj = self.get_object(request, unquote(object_id))

        if obj:
            context.update({
                'title': force_text(obj.plugin),
            })

        return super(FormSubmissionAdmin, self).change_view(
            request, object_id, form_url=form_url,
            extra_context=context)

    def export_view(self, request, form_url=''):
        """The 'export' admin view for this model."""

        info = self.opts.app_label, self.opts.model_name

        if not self.has_export_permission(request):
            raise PermissionDenied

        form = SubmissionExportForm(data=request.POST if request.method == 'POST' else None)

        if form.is_valid():
            data = form.cleaned_data
            queryset = self.get_queryset(request) \
                .filter(plugin_id=data.get('form')) \
                .select_related('created_by', 'plugin', )

            from_date, to_date = data.get('from_date'), data.get('to_date')
            headers = data.get('headers', [])

            if from_date:
                queryset = queryset.filter(creation_date__gte=from_date)
            if to_date:
                queryset = queryset.filter(creation_date__lt=to_date + datetime.timedelta(days=1))

            if not queryset.exists():
                message = _('No matching %s found for the given criteria. '
                            'Please try again.') % self.opts.verbose_name_plural
                self.message_user(request, message, level=messages.WARNING)
                if request.is_ajax():
                    data = {
                        'reloadBrowser': True,
                        'submissionCount': 0,
                    }
                    return JsonResponse(data)
                return redirect('admin:%s_%s_export' % info)

            latest_submission = queryset[:1].get()
            dataset = Dataset(title=Truncator(latest_submission.plugin.name).chars(31))

            if not headers:
                headers = [field['label'].strip() for field in latest_submission.form_data]
                for submission in queryset:
                    for field in submission.form_data:
                        label = field['label'].strip()
                        if label not in headers:
                            headers.append(label)

                if request.is_ajax():
                    data = {
                        'reloadBrowser': False,
                        'submissionCount': queryset.count(),
                        'availableHeaders': headers,
                    }
                    return JsonResponse(data)

            headers.extend(['Submitted By', 'Submitted on', 'Sender IP', 'Referrer URL'])
            dataset.headers = headers

            def humanize(field):
                value = field['value']
                field_type = field['type']

                if value in (None, '', [], (), {}):
                    return None

                if field_type == 'checkbox':
                    value = yesno(bool(value), u'{0},{1}'.format(_('Yes'), _('No')))
                if field_type == 'checkbox_multiple':
                    value = ', '.join(list(value))
                return value

            for submission in queryset:
                row = [None] * len(headers)
                for field in submission.form_data:
                    label = field['label'].strip()
                    if label in headers:
                        row[headers.index(label)] = humanize(field)

                    row[-4] = force_text(submission.created_by or _('Unknown')) 
                    row[-3] = submission.creation_date.strftime(
                        settings.DJANGOCMS_FORMS_DATETIME_FORMAT)
                    row[-2] = submission.ip
                    row[-1] = submission.referrer
                dataset.append(row)

            mimetype = {
                'xls': 'application/vnd.ms-excel',
                'csv': 'text/csv',
                'html': 'text/html',
                'yaml': 'text/yaml',
                'json': 'application/json',
            }

            file_type = data.get('file_type', 'xls')
            filename = settings.DJANGOCMS_FORMS_EXPORT_FILENAME.format(
                form_name=slugify(latest_submission.plugin.name))
            filename = timezone.now().strftime(filename)
            filename = '%s.%s' % (filename, file_type)

            response = HttpResponse(
                getattr(dataset, file_type), {
                    'content_type': mimetype.get(file_type, 'application/octet-stream')
                })

            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response

        # Wrap in all admin layout
        fieldsets = ((None, {'fields': form.fields.keys()}),)
        adminform = AdminForm(form, fieldsets, {}, model_admin=self)
        media = self.media + adminform.media

        context = {
            'title': _('Export %s') % force_text(self.opts.verbose_name_plural),
            'adminform': adminform,
            'is_popup': (IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET),
            'media': mark_safe(media),
            'errors': AdminErrorList(form, ()),
            'app_label': self.opts.app_label,
        }
        return self.render_export_form(request, context, form_url)

    def render_export_form(self, request, context, form_url=''):
        """
        Render the from submission export form.
        """
        context.update({
            'has_change_permission': self.has_change_permission(request),
            'form_url': mark_safe(form_url),
            'opts': self.opts,
            'add': True,
            'save_on_top': self.save_on_top,
        })

        return TemplateResponse(request, self.export_form_template, context)


admin.site.register(FormSubmission, FormSubmissionAdmin)
