# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import djangocms_forms.fields
import django.db.models.deletion
import cms.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=255, editable=False, db_index=True)),
            ],
            options={
                'verbose_name': 'Form',
                'verbose_name_plural': 'Forms',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormDefinition',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('name', models.CharField(max_length=255, verbose_name='Form Name')),
                ('title', models.CharField(max_length=150, verbose_name='Title', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('submit_btn_txt', models.CharField(default='Submit', help_text="Text for the Submit Button. The default is 'Submit'", max_length=100, verbose_name='Submit Button Text')),
                ('post_submit_msg', models.TextField(default='Thank You', help_text='Display this message to users after they submit your form.', verbose_name='Post Submit Message', blank=True)),
                ('success_redirect', models.BooleanField(default=False, help_text='HTTP redirect after successful submission', verbose_name='Redirect?')),
                ('external_redirect', models.URLField(help_text='e.g. http://example.com/thank-you', verbose_name='External URL', blank=True)),
                ('email_to', models.CharField(help_text='Separate several addresses with a comma.', max_length=255, verbose_name='Send form data to e-mail address', blank=True)),
                ('email_from', models.EmailField(max_length=255, verbose_name='Sender Email Address', blank=True)),
                ('email_subject', models.CharField(max_length=255, verbose_name='Email Subject', blank=True)),
                ('email_uploaded_files', models.BooleanField(default=True, verbose_name='Send uploaded files as email attachments')),
                ('save_data', models.BooleanField(default=True, help_text='Logs all form submissions to the database.', verbose_name='Save to database')),
                ('spam_protection', models.SmallIntegerField(default=0, verbose_name='Spam Protection', choices=[(0, 'None'), (1, 'Honeypot'), (2, 'ReCAPTCHA')])),
                ('form_template', models.CharField(default=b'djangocms_forms/form_template/default.html', max_length=150, verbose_name='Form Template', blank=True, choices=[(b'djangocms_forms/form_template/default.html', 'Default')])),
                ('page_redirect', cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cms.Page', help_text='A page has priority over an external URL', null=True, verbose_name='Page URL')),
                ('plugin_reference', djangocms_forms.fields.PluginReferenceField(related_name='plugin', on_delete=django.db.models.deletion.SET_NULL, editable=False, to='djangocms_forms.Form', null=True)),
            ],
            options={
                'verbose_name': 'Form',
                'verbose_name_plural': 'Forms',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_type', models.CharField(default=b'text', max_length=100, verbose_name='Field Type', choices=[(b'text', 'Text'), (b'textarea', 'Text Area'), (b'email', 'Email'), (b'number', 'Number'), (b'phone', 'Phone'), (b'url', 'URL'), (b'checkbox', 'Checkbox'), (b'checkbox_multiple', 'Multi Checkbox'), (b'select', 'Drop down'), (b'radio', 'Radio'), (b'file', 'File Upload'), (b'date', 'Date'), (b'time', 'Time'), (b'password', 'Password'), (b'hidden', 'Hidden')])),
                ('label', models.CharField(max_length=255, verbose_name='name')),
                ('placeholder_text', models.CharField(max_length=100, verbose_name='Placeholder Text', blank=True)),
                ('required', models.BooleanField(default=True, verbose_name='Required')),
                ('help_text', models.TextField(help_text='A description / instructions for this field.', verbose_name='Description', blank=True)),
                ('initial', models.CharField(max_length=255, verbose_name='Default Value', blank=True)),
                ('choice_values', models.TextField(help_text='Enter options one per line. For "File Upload" field type, enter allowed filetype (e.g .pdf) one per line.', verbose_name='Choices', blank=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='Position', blank=True)),
                ('form', models.ForeignKey(related_name='fields', to='djangocms_forms.FormDefinition')),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'field',
                'verbose_name_plural': 'fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name='Date')),
                ('ip', models.GenericIPAddressField(null=True, verbose_name=b'IP', blank=True)),
                ('form_data', jsonfield.fields.JSONField(verbose_name='Form Data')),
                ('created_by', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='User')),
                ('plugin', models.ForeignKey(related_name='submissions', editable=False, to='djangocms_forms.Form', verbose_name='Form')),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'Form Submission',
                'verbose_name_plural': 'Form Submissions',
            },
            bases=(models.Model,),
        ),
    ]
