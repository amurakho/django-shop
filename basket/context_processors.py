from main import models as product_models


def get_products_in_basket(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    try:
        basket = product_models.Bucket.objects.get(session_key=session_key)
    except:
        return {'products_in_basket': None}
    _, count = basket.make_full_data()
    return {'products_in_basket': basket.products.all(),
            'full_count': count}

