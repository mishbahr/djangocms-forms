(function($) {
    $(function() {
        var form = $('#formsubmission_form'),
            formSelectorInput = $('select[id="id_form"]', form),
            headersFieldWrapper = $('.field-headers', form);

        var fetchAvailableHeaders = function() {
            if (!formSelectorInput.val()) {
                headersFieldWrapper.slideUp('fast');
                return;
            }

            var data = {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]', form).val(),
                'form': formSelectorInput.val(),
                'file_type': $('select[id="id_file_type"]', form).val()
            };

            $.ajax({
                type: 'POST',
                data: data,
                success: function(response) {
                    if (response.reloadBrowser) {
                        location.reload(true);
                    }
                    var headersInput__from = $('select[id="id_headers_from"]', form),
                        headersInput__to = $('select[id="id_headers_to"]', form);

                    headersInput__to.find('option').remove();
                    headersInput__from.find('option').remove();

                    $.each(response.availableHeaders, function(index, value) {
                        headersInput__from.append($('<option/>', {
                            value: value,
                            text: value
                        }));
                    });

                    SelectBox.init('id_headers_from');
                    SelectBox.init('id_headers_to');
                    headersFieldWrapper.slideDown();
                },
                error: function() {
                    alert('We\'re sorry. Something unexpected happened. Please reload the page and try again.');
                }
            });

            return false;
        };

        if ($('body').hasClass('export-form')) {
            fetchAvailableHeaders();
            formSelectorInput.change(fetchAvailableHeaders);
        }
    });
})(django.jQuery);
