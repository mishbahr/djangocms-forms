// the semi-colon before function invocation is a safety net against concatenated
// scripts and/or other plugins which may not be closed properly.
;(function($, window, document, undefined) {

    var cmsForms = 'cmsForms',
        defaults = {
            formWrapper: '.form-wrapper',
            formErrors: '.form-errors',
            formSuccess: '.form-success',
            fieldWrapper: '.field-wrapper',
            fieldErrors: '.field-errors',

            errorClass: 'error',
            errorList: '<ul class="errorlist"></ul>',
            errorItem: '<li></li>',
            ajaxErrorMsg: 'We\'re sorry. Something Unexpected Happened. Please Try Again Later.',

            reCaptchaSiteKey: '',
            reCaptchaTheme: 'light',
            reCaptchaSize: 'normal',

            // needed in case someone overrides the template and doesn't pass
            // in the value when initializing the cmsForms object
            redirectDelay: 1000
        };

    function CMSForms(el, options) {
        this.el = $(el);
        this.settings = $.extend({}, defaults, options);
        this._defaults = defaults;
        this._name = cmsForms;

        this.init();
    }

    CMSForms.prototype = {
        init: function() {
            this.form = this.getForm();
            var ajaxOptions = {
                type: 'POST',
                success: $.proxy(this.ajaxSuccess, this),
                error: $.proxy(this.ajaxError, this)
            };
            this.form.on('submit', function(e) {
                e.preventDefault();
                $(this).ajaxSubmit(ajaxOptions);
            });

            if (typeof(grecaptcha) == 'undefined') {
                window.reCapctchaOnloadCallback = function() {
                    this.renderReCaptcha();
                }.bind(this);
            } else {
                this.renderReCaptcha();
            }
        },
        getForm: function() {
            return $('form', this.el);
        },
        renderReCaptcha: function() {
            var that = this;
            $('.g-recaptcha').each(function() {
                var widgetId = $(this).attr('id');
                grecaptcha.render(widgetId, {
                    sitekey: that.settings.reCaptchaSiteKey,
                    size: that.settings.reCaptchaSize,
                    theme: that.settings.reCaptchaTheme
                });
            });
        },
        ajaxSuccess: function(response) {
            if (response.formIsValid) this.formValid(response);
            else this.formInvalid(response);
        },
        ajaxError: function() {
            this.resetForm();

            var formErrors = $(this.settings.errorList);
            $(this.settings.errorItem).html(this.settings.ajaxErrorMsg).appendTo(formErrors);
            this.form.find(this.settings.formErrors).append(formErrors).fadeIn('slow');
        },
        resetForm: function() {
            this.form.find(this.settings.formErrors).fadeOut().empty();
            this.form.find(this.settings.fieldErrors).fadeOut().empty();
            this.form.find(this.settings.fieldWrapper).removeClass(this.settings.errorClass);

            if (typeof(grecaptcha) != 'undefined') {
                grecaptcha.reset();
            }
        },
        formValid: function(response) {
            $(this.settings.formSuccess, this.el).fadeIn('slow');
            $(this.settings.formWrapper, this.el).slideUp('slow').remove();
            if (response.redirectUrl) {
                setTimeout(function() {
                    window.location = response.redirectUrl;
                }, this.settings.redirectDelay);
            }
        },
        formInvalid: function(response) {
            this.resetForm();

            $.each(response.errors, function(name, errorList) {
                if (name == '__all__') {
                    // NON_FIELD_ERRORS
                    var formErrors = $(this.settings.errorList);
                    errorList.forEach(function(error) {
                        $(this.settings.errorItem).text(error).appendTo(formErrors);
                    }.bind(this));
                    this.form.find(this.settings.formErrors).append(formErrors).fadeIn('slow');
                } else {
                    var isRecapcha = name.match('^recaptcha');
                    var formInput = (isRecapcha) ? '.g-recaptcha' : ':input[name=' + name + ']';
                    var formField = this.form.find(formInput).first();
                    var fieldWrapper = formField.parents(this.settings.fieldWrapper).addClass(this.settings.errorClass);

                    var fieldErrors = $(this.settings.errorList);
                    errorList.forEach(function(error) {
                        $(this.settings.errorItem).text(error).appendTo(fieldErrors);
                    }.bind(this));
                    fieldWrapper.find(this.settings.fieldErrors).append(fieldErrors).fadeIn('slow');
                }
            }.bind(this));
        }
    };

    $.fn[cmsForms] = function(options) {
        return this.each(function() {
            if (!$.data(this, 'plugin_' + cmsForms)) {
                $.data(this, 'plugin_' + cmsForms, new CMSForms(this, options));
            }
        });
    };

})(jQuery, window, document);
