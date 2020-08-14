



from django.dispatch import Signal

form_submission = Signal(providing_args=['form', 'cleaned_data'])
