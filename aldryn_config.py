


from aldryn_client import forms


class Form(forms.BaseForm):
    plugin_module = forms.CharField('Plugin module name', initial='Generic')
    plugin_name = forms.CharField('Plugin name', initial='Form')
    html5_required = forms.CheckboxField(
        'Use HTML5 required?', initial=False, required=False,
        help_text='If checked, all required fields inputs will be rendered '
                  'with HTML5 "required=required" attribute')
    recaptcha_public_key = forms.CharField('ReCaptcha Site Key', required=False)
    recaptcha_secret_key = forms.CharField('ReCaptcha Secret Key', required=False)

    def to_settings(self, data, settings):
        settings['DJANGOCMS_FORMS_PLUGIN_MODULE'] = data['plugin_module']
        settings['DJANGOCMS_FORMS_PLUGIN_NAME'] = data['plugin_name']
        settings['DJANGOCMS_FORMS_USE_HTML5_REQUIRED'] = data['html5_required']
        settings['DJANGOCMS_FORMS_RECAPTCHA_PUBLIC_KEY'] = data['recaptcha_public_key']
        settings['DJANGOCMS_FORMS_RECAPTCHA_SECRET_KEY'] = data['recaptcha_secret_key']
        return settings
