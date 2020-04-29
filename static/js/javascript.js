
$(document).ready(function () {
    function filter(e) {
        e.preventDefault();

        var active_btn = $(document.activeElement)
        if (active_btn.hasClass('sort-btn')){
            $(this).parent().find('button').each(function () {
                $(this).attr('id', '')
            })
            active_btn.attr('id', 'pressed')
        }
        else{
            if (active_btn.attr('id') == 'pressed'){
                active_btn.attr('id', '')
                active_btn.parent().css('background-color', '')
            }
            else {
                active_btn.attr('id', 'pressed')
            }
        }

        var pressed_buttons = $("*#pressed");
        var cat_array = []
        var sort = NaN
        $.each(pressed_buttons, function () {
            if ($(this).parent().attr('id') == 'sort'){
                sort = $(this).attr('value')
            }
            else{
                cat_array.push($(this).attr('value'))
                $(this).parent().css('background-color', 'rgba(181,152,152,0.45)')
            }
        })

        $.ajax({
            traditional: true,
            method: "GET",
            url: $(this).attr('action'),
            data: {
                'sort': sort,
                'categories': cat_array,
                'search_value': search_value
            },
            dataType: "json",
            success: function (response) {
                $('#list-block').html(response['html']);
            }
        })
    }
    $('#sort').submit(filter);
    $('#categories').submit(filter);
})