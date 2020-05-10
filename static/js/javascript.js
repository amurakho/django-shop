
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

    function buy(e){
        e.preventDefault();
        var tmp = $(this).attr('action')

        $.ajax({
            method: 'POST',
            url: $(this).attr('action'),
            data:{
                'product': $('#product').val(),
                'count': $('#count').val(),
            },
            dataType: 'json',
            success: function (data) {
                $('#bucket-count span').html('')
                $('#bucket-count span').append(data.products_number)

                if (!$('#basket-items').length){
                    $('#basket-container').append(
                        '<div class="basket-items d-none" id="basket-items">' +
                            '<ul></ul>' +
                            '<a href="#">Оформить заказ</a>' +
                        '</div>'
                    )
                }
                else{
                    $('#basket-container ul').html('')
                }
                console.log(tmp)
                $.each(data.products_in_bucket, function (key, val) {
                        // var tmp = $(this).attr('action')
                        $('#basket-container ul').append(
                            '<div class="d-flex">' +
                            '<h6>' + val.name + ' ' + val.count + ' ' + val.full_price +' грн.' + '</h6>' +
                            '<a href="'+val.url+'">X</a>' +
                            '</div>'
                        )
                    })
            }
        })
    }

    function remove_delivery_hide(id_list) {
        id_list.forEach((element) => {
            $('#'+element).removeClass('d-none')
            $('#'+element + ' input').prop('required', true);
        })
    }

    function add_delivery_hide(id_list) {
        id_list.forEach((element) => {
            $('#'+element).addClass('d-none')
            $('#'+element + ' input').prop('required', false);
        })
    }

    function delivery_choice(e){
        if (this.value == 'new_post'){
            remove_delivery_hide(['new-post'])
            add_delivery_hide(['ukr-post', 'courier-delivery'])
        }
        else if (this.value == 'ukr_post'){
            remove_delivery_hide(['ukr-post', 'courier-delivery'])
            add_delivery_hide(['new-post'])
        }
        else if (this.value == 'new_post_courier'){
            remove_delivery_hide(['courier-delivery'])
            add_delivery_hide(['ukr-post', 'new-post'])
        }
    }

    $('#basket-container').on('click', function (e) {
        // e.preventDefault();
        $('#basket-items').removeClass('d-none')
    });
    $('#basket-container').mouseover(function (e) {
        $('#basket-items').removeClass('d-none')
    });
    $('#basket-container #basket-items').mouseout(function (e) {
        $('#basket-items').addClass('d-none')
    });

    $('#sort').submit(filter);
    $('#categories').submit(filter);

    $('#buy-item').submit(buy);

    $('#delivery-choice').change(delivery_choice);

})

