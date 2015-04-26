jQuery(function($) {
    var target = $('div.inline-group');
    var item = 'div.inline-related';
    var typeInput = 'select[id*=-field_type]';

    var init = function() {
        target.find(item).each(function() {
            var that = $(this);
            var inputField = that.find(typeInput);
            var toggleField = function() {
                var selectedFieldType = inputField.val();
                var choiceFields = ['checkbox_multiple', 'select', 'radio', 'file'];
                var showChoiceField = $.inArray(selectedFieldType, choiceFields) >= 0;
                that.find('.field-choice_values')
                    .toggle(showChoiceField)
                    .toggleClass('required', showChoiceField);

                that.find('.field-placeholder_text, .field-help_text, .field-choice_values:not(:hidden)')
                    .toggle(selectedFieldType != 'hidden')

            };
            inputField.change(function() {
                toggleField();
            });
            toggleField();
        })
    };

    init();

    // init again when "Add another" link is clicked
    $('.add-row a').click(function() {
        init();
    })
});
