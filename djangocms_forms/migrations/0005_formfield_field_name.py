# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_forms', '0004_redirect_delay'),
    ]

    operations = [
        migrations.AddField(
            model_name='formfield',
            name='field_name',
            field=models.CharField(max_length=255, verbose_name='Custom Field Name', blank=True),
        ),
    ]
