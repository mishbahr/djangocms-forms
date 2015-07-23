# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='form',
            options={'verbose_name': 'form', 'verbose_name_plural': 'forms'},
        ),
        migrations.AlterModelOptions(
            name='formdefinition',
            options={'verbose_name': 'form', 'verbose_name_plural': 'forms'},
        ),
        migrations.AlterModelOptions(
            name='formsubmission',
            options={'ordering': ('-creation_date',), 'verbose_name': 'form submission', 'verbose_name_plural': 'form submissions', 'permissions': (('export_formsubmission', 'Can export Form Submission'),)},
        ),
    ]
