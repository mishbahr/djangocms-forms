from django import forms, template
from django.template.defaultfilters import yesno
from django.utils.safestring import mark_safe
from django.utils.six import string_types
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from djangocms_forms.fields import HoneyPotField

register = template.Library()


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_password(field):
    return isinstance(field.field.widget, forms.PasswordInput)


@register.filter
def is_radioselect(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_select(field):
    return isinstance(field.field.widget, forms.Select)


@register.filter
def is_checkboxselectmultiple(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.ClearableFileInput)


@register.filter
def is_honeypot(field):
    return isinstance(field.field, HoneyPotField)


@register.filter
def is_required(field):
    return field.field.required


@register.filter
def classes(field):
    """
    Returns CSS classes of a field
    """
    return field.widget.attrs.get('class', None)


@register.filter
def input_class(field):
    """
    Returns widgets class name in lowercase
    """
    return field.field.widget.__class__.__name__.lower()


@register.filter
def friendly(value):
    if value in (None, '', [], (), {}):
        return None

    if type(value) is list:
        value = ', '.join(value)
    if type(value) is bool:
        value = yesno(value, u'{0},{1}'.format(_('Yes'), _('No')))
    if not isinstance(value, string_types):
        value = force_text(value)
    return value


@register.filter
def to_html(field):
    value = field['value']
    field_type = field['type']

    if value in (None, '', [], (), {}):
        return mark_safe('&mdash;')

    if field_type == 'file':
        value = '<a href="{0}">{0}</a>'.format(value)
    if field_type == 'checkbox':
        value = yesno(bool(value), u'{0},{1}'.format(_('Yes'), _('No')))
    if field_type == 'checkbox_multiple':
        value = ', '.join(list(value))
    return mark_safe(value)
