import re

from django import forms
from django.contrib.admin.widgets import (AdminDateWidget,
                                          FilteredSelectMultiple)
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from ipware.ip import get_ip
from unidecode import unidecode

from .fields import FormBuilderFileField, MultipleChoiceAutoCompleteField
from .models import Form, FormDefinition, FormField, FormSubmission
from .widgets import DateInput, TelephoneInput, TimeInput


class FormFieldInlineForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(FormFieldInlineForm, self).clean()

        requires_choice_values = ['checkbox_multiple', 'select', 'radio']
        if (cleaned_data.get('field_type') in requires_choice_values and
                not cleaned_data.get('choice_values')):

            error_msg = _('This field is required.')
            self._errors['choice_values'] = self.error_class([error_msg])

        return cleaned_data

    class Meta:
        model = FormField
        fields = '__all__'


class FormDefinitionAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(FormDefinitionAdminForm, self).clean()

        populated_count = 0
        storage_fields = ('email_to', 'save_data', )

        for field in storage_fields:
            if cleaned_data.get(field, None):
                populated_count += 1

        if not populated_count:
            error_msg = _(
                'You must choose a storage option for this Form. '
                'You can choose to use multiple storage options if you prefer. ')
            for field in storage_fields:
                self._errors[field] = self.error_class([error_msg])

        return cleaned_data

    class Meta:
        model = FormDefinition
        fields = '__all__'


class FormBuilder(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'

    form_id = forms.CharField(widget=forms.HiddenInput)
    current_page = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, form_definition, *args, **kwargs):
        super(FormBuilder, self).__init__(*args, **kwargs)
        self.form_definition = form_definition
        self.field_names = []
        self.file_fields = []
        self.field_types = {}

        self.submission_url = reverse('djangocms_forms_submissions')
        self.fields['form_id'].initial = form_definition.pk
        self.redirect_url = form_definition.redirect_url

        for field in form_definition.fields.all():
            if hasattr(self, 'prepare_%s' % field.field_type):
                field_name = self.get_unique_field_name(field)
                form_field = getattr(self, 'prepare_%s' % field.field_type)(field)

                self.fields[field_name] = form_field

                if isinstance(form_field, FormBuilderFileField):
                    self.file_fields.append(field_name)

    def get_unique_field_name(self, field):
        field_name = '%s' % (slugify(unidecode(field.label)).replace('-', '_'))
        if field_name in self.field_names:
            i = 1
            while True:
                if i > 1:
                    if i > 2:
                        field_name = field_name.rsplit('_', 1)[0]
                    field_name = '%s_%s' % (field_name, i)
                if field_name not in self.field_names:
                    break
                i += 1

        self.field_names.append(field_name)
        self.field_types[field_name] = field.field_type
        return field_name

    def split_choices(self, choices):
        return [x.strip() for x in choices.split(',') if x.strip()]

    def to_bool(self, value):
        return value.lower() in ('yes', 'y', 'true', 't', '1')

    def prepare_text(self, field):
        kwargs = field.field_attrs()
        if field.placeholder_text and not field.initial:
            kwargs.update({
                'widget': forms.TextInput({
                    'placeholder': field.placeholder_text
                })
            })
        return forms.CharField(**kwargs)

    def prepare_textarea(self, field):
        kwargs = field.field_attrs()
        kwargs.update({
            'widget': forms.Textarea({
                'placeholder': field.placeholder_text or '',
            })
        })
        return forms.CharField(**kwargs)

    def prepare_email(self, field):
        kwargs = field.field_attrs()
        kwargs.update({
            'widget': forms.EmailInput({
                'placeholder': field.placeholder_text or '',
                'autocomplete': 'email',
            }),
        })
        return forms.EmailField(**kwargs)

    def prepare_checkbox(self, field):
        kwargs = field.field_attrs()
        if field.initial:
            kwargs.update({
                'initial': self.to_bool(field.initial)
            })
        return forms.BooleanField(**kwargs)

    def prepare_checkbox_multiple(self, field):
        kwargs = field.field_attrs()
        kwargs.update({
            'widget': forms.CheckboxSelectMultiple(),
            'choices': field.get_choices(),
        })

        if field.initial:
            kwargs.update({
                'initial': self.split_choices(field.initial)
            })
        return forms.MultipleChoiceField(**kwargs)

    def prepare_select(self, field):
        kwargs = field.field_attrs()
        if field.choice_values:
            choice_list = field.get_choices()
            if not field.required:
                choice_list.insert(0, ('', field.placeholder_text or _('Please select an option')))
            kwargs.update({
                'choices': choice_list
            })
        return forms.ChoiceField(**kwargs)

    def prepare_radio(self, field):
        kwargs = field.field_attrs()
        kwargs.update({
            'widget': forms.RadioSelect(),
            'choices': field.get_choices(),
        })
        return forms.ChoiceField(**kwargs)

    def prepare_file(self, field):
        kwargs = field.field_attrs()
        if field.choice_values:
            regex = re.compile('[\s]*\n[\s]*')
            choices = regex.split(field.choice_values)
            kwargs.update({
                'allowed_file_types': [i.lstrip('.').lower() for i in choices]
            })
        return FormBuilderFileField(**kwargs)

    def prepare_date(self, field):
        kwargs = field.field_attrs()
        kwargs.update({
            'widget': DateInput(),
        })
        return forms.DateField(**kwargs)

    def prepare_time(self, field):
        # @todo: needs proper widget
        kwargs = field.field_attrs()
        kwargs.update({
            'widget': TimeInput(),
        })
        return forms.TimeField(**kwargs)

    def prepare_hidden(self, field):
        kwargs = field.field_attrs()
        kwargs.update({
            'widget': forms.HiddenInput(),
        })
        return forms.CharField(**kwargs)

    def prepare_number(self, field):
        kwargs = field.field_attrs()
        return forms.IntegerField(**kwargs)

    def prepare_url(self, field):
        kwargs = field.field_attrs()
        return forms.URLField(**kwargs)

    def prepare_password(self, field):
        kwargs = field.field_attrs()
        kwargs.update({
            'widget': forms.PasswordInput(),
        })
        return forms.CharField(**kwargs)

    def prepare_phone(self, field):
        kwargs = field.field_attrs()
        kwargs.update({
            'widget': TelephoneInput(),
        })
        return forms.CharField(**kwargs)

    def save(self, request):
        form_data = []
        for field in self.field_names:
            value = self.cleaned_data[field]
            if hasattr(value, 'url'):
                value = value.url
            form_data.append({
                'name': field,
                'label': self.fields[field].label,
                'value': value,
                'type': self.field_types[field],
            })
        if self.form_definition.save_data:
            self.save_to_db(form_data, request=request)
        if self.form_definition.email_to:
            self.email_submission(form_data, request=request)

    def save_to_db(self, form_data, request):
        user = request.user if request.user.is_authenticated() else None
        FormSubmission.objects.create(
            plugin=self.form_definition.plugin_reference,
            ip=get_ip(request),
            form_data=form_data,
            created_by=user)

    def email_submission(self, form_data, request):
        mail_to = re.compile('\s*[,;]+\s*').split(self.form_definition.email_to)
        mail_from = self.form_definition.email_from or None
        mail_subject = self.form_definition.email_subject or \
            'Form Submission - %s' % self.form_definition.name
        context = {
            'form': self.form_definition,
            'title': mail_subject,
            'form_data': form_data,
            'request': request,
            'recipients': mail_to,
        }

        message = render_to_string('djangocms_forms/email_template/email.txt', context)
        message_html = render_to_string('djangocms_forms/email_template/email.html', context)

        email = EmailMultiAlternatives(mail_subject, message, mail_from, mail_to)
        email.attach_alternative(message_html, 'text/html')

        if self.files and self.form_definition.email_uploaded_files:
            for file_path in self.files:
                email.attach_file(file_path)

        email.send(fail_silently=False)


class SubmissionExportForm(forms.Form):
    FORMAT_CHOICES = (
        ('csv', _('CSV')),
        ('json', _('JSON')),
        ('yaml', _('YAML')),
        ('xls', _('Microsoft Excel')),
    )

    form = forms.ModelChoiceField(
        queryset=Form.active_objects.all(), label=_('Select a Form'),
        error_messages={'required': _('Please select a form.')},
        help_text=_('Select the form you would like to export entry data from. '
                    'You may only export data from one form at a time.'))
    file_type = forms.ChoiceField(choices=FORMAT_CHOICES, initial='xls', required=False)
    headers = MultipleChoiceAutoCompleteField(
        label=_('Fields'), required=False,
        widget=FilteredSelectMultiple(verbose_name=_('Fields'), is_stacked=False),)
    from_date = forms.DateField(
        label=_('From date'), required=False, widget=AdminDateWidget)
    to_date = forms.DateField(
        label=_('To date'), required=False, widget=AdminDateWidget)
