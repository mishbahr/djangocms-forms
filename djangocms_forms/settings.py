from django.utils.translation import ugettext_lazy as _

TEXT = 'text'
TEXTAREA = 'textarea'
EMAIL = 'email'
CHECKBOX = 'checkbox'
CHECKBOX_MULTIPLE = 'checkbox_multiple'
SELECT = 'select'
RADIO = 'radio'
FILE = 'file'
DATE = 'date'
TIME = 'time'
HIDDEN = 'hidden'
NUMBER = 'number'
URL = 'url'
PASSWORD = 'password'
PHONE = 'phone'

FIELD_TYPES = (
    (TEXT, _('Text')),
    (TEXTAREA, _('Text Area')),
    (EMAIL, _('Email')),
    (NUMBER, _('Number')),
    (PHONE, _('Phone')),
    (URL, _('URL')),
    (CHECKBOX, _('Checkbox')),
    (CHECKBOX_MULTIPLE, _('Multi Checkbox')),
    (SELECT, _('Drop down')),
    (RADIO, _('Radio')),
    (FILE, _('File Upload')),
    (DATE, _('Date')),
    (TIME, _('Time')),
    (PASSWORD, _('Password')),
    (HIDDEN, _('Hidden')),
)
