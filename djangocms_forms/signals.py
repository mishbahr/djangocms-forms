# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.dispatch import Signal

form_submission = Signal(providing_args=['form', 'cleaned_data'])
