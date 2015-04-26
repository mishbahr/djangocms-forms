/*
Replaces the name in an inline element's header while typing it in the input of the "name" field.
This way, the extra inline element's header will be named instead of numbered #4, #5 etc.
*/

jQuery(function($) {

    var target = $('div.inline-group');
    var item = 'div.inline-related';
    var nameInput = 'input[id*=-label]';
    var typeInput = 'select[id*=-field_type]';


    var init = function() {
        target.find(item).each(function() {
            var nameField = $(this).find(nameInput);
            var typeField = $(this).find(typeInput);
            var label = $('.inline_label', this);
            var rename = function() {
                if (nameField.val()) {
                    label.text(nameField.val());
                }
                else {
                    label.text(typeField.find('option:selected').text() + ' Field');
                }
            };
            nameField.keyup(function(event) {
                // Update name while typing
                rename();
            });

            typeField.change(function(){
                rename();
            });
            rename();
        })
    }

    init();

    // init again when "Add another" link is clicked
    $('.add-row a').click(function() {
        init();
    })
});
