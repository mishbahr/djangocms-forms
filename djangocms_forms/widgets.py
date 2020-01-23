# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.forms import widgets


class TelephoneInput(widgets.TextInput):
    input_type = "tel"


class SearchInput(widgets.TextInput):
    input_type = "search"


class DateInput(widgets.TextInput):
    input_type = "date"


class TimeInput(widgets.TextInput):
    input_type = "time"
