# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_forms', '0003_add_referrer_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='formdefinition',
            name='redirect_delay',
            field=models.PositiveIntegerField(verbose_name='Redirect Delay', blank=True, null=True, help_text="Wait this number of milliseconds before redirecting. 1000 milliseconds = 1 second."),
        ),
    ]
