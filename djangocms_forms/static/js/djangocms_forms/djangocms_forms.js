(function ($) {
    $.fn.djangocms_forms = function (options) {
        if (options === undefined) { options = {}; }

        var defaults = {
            form_wrapper: '.form-wrapper',
            field_wrapper: '.field-wrapper',
            form_errors: '.form-errors',
            field_errors: '.field-errors',
            form_success: '.form-success',
            errorlist_css_class: 'errorlist',
            error_css_class: 'error',
            server_error: 'We\'re sorry. Something Unexpected Happened. Please Try Again Later.'
        };

        this.each(function(options) {
            var options = $.extend( {}, defaults, options) ;

            var el = $(this),
                form_wrapper = $(options.form_wrapper, el),
                form_success = $(options.form_success, el),
                form = $('form', form_wrapper);


            function clearErrors() {
                form.find(options.form_errors).fadeOut().empty(); //clear form errors
                form.find(options.field_errors).fadeOut().empty(); //clear field errors
                form.find(options.field_wrapper).removeClass(options.error_css_class); //remove error classes
            }

            // post-submit callback
            function ajaxSuccess(response) {
                if (response.status == 'success'){
                    formValid(response.redirect_url);
                }
                else if (response.status == 'error'){
                    formInvalid(response.form_errors);
                }
            }

            function formValid(success_url) {
                form_success.fadeIn('slow');
                form_wrapper.slideUp('slow').remove();

                if (success_url){
                    setTimeout(function(){
                        window.location = success_url;
                    }, 1000);
                }

            }

            function formInvalid(form_errors) {
                clearErrors()
                $.each(form_errors, function(key, value) {
                    var field = form.find(':input[name=' + key + ']').first();
                    var field_wrapper = field.parents(options.field_wrapper).addClass(options.error_css_class);
                    var field_error = $('<ul/>').addClass(options.errorlist_css_class);
                    $.each(value, function(key, value) {
                        $('<li>', {
                            text: value
                        }).appendTo(field_error);
                    });
                    field_wrapper.find(options.field_errors).append(field_error).fadeIn('slow')
                });
                if (form_errors.__all__) {
                    var form_error = $('<ul/>').addClass(options.errorlist_css_class);
                    $.each(form_errors.__all__, function(key, value) {
                        $('<li>', {
                            text: value
                        }).appendTo(form_error);
                    });
                    form.find(options.form_errors).append(form_error).fadeIn('slow');
                }
            }

            function ajaxError() {
                clearErrors();
                var form_error = $('<ul/>').addClass(options.error_class);
                $('<li>', {
                    html: options.server_error
                }).appendTo(form_error);
                form.find(options.form_errors).append(form_error).fadeIn('slow');
            }

            // attach handler to form's submit event
            form.submit(function () {
                var ajaxOptions = {
                    type: 'POST',
                    success: ajaxSuccess,
                    error: ajaxError
                };
                // submit the form
                $(this).ajaxSubmit(ajaxOptions);
                // return false to prevent normal browser submit and page navigation
                return false;
            });
        });
    };
})(jQuery);
