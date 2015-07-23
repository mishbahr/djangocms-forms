# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_forms', '0002_alter_model_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='formsubmission',
            name='referrer',
            field=models.CharField(max_length=150, verbose_name='Referrer URL', blank=True),
        ),
    ]
