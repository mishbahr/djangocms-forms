from django.forms.widgets import TextInput


class TelephoneInput(TextInput):
    input_type = 'tel'


class SearchInput(TextInput):
    input_type = 'search'


class DateInput(TextInput):
    input_type = 'date'


class TimeInput(TextInput):
    input_type = 'time'
