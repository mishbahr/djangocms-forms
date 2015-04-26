(function($) {
    $(function() {
        var formsubmission_form = $('#formsubmission_form');
        var form_field = $('select[id="id_form"]', formsubmission_form);
        var headers_field = $('.field-headers', formsubmission_form);

        var loadHeaders = function() {
            if (!form_field.val()) {
                headers_field.slideUp('fast');
                return;
            }

            var data = {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'form': $('select[name="form"]').val(),
                'file_type': $('select[name="file_type"]').val()
            };

            $.ajax({
                type: 'POST',
                url: '',
                data: data,
                success: function(response) {
                    if (response.reloadBrowser) {
                        location.reload();
                    }
                    $('select[id="id_headers_to"]').find('option').remove();

                    var headers_input_from = $('select[id="id_headers_from"]');
                    headers_input_from.find('option').remove();

                    $.each(response.availableHeaders, function(index, value) {
                        headers_input_from.append('<option value=' + value + '>' + value + '</option>');
                    });

                    SelectBox.init('id_headers_from');
                    SelectBox.init('id_headers_to');
                    headers_field.slideDown();
                },
                error: function() {
                    alert('We\'re sorry. Something unexpected happened. Please reload the page and try again.');
                }
            });

            return false;
        };

        if ($('body').hasClass('export-form')) {
            loadHeaders();
            form_field.change(loadHeaders);
        }
    });
})(django.jQuery);
