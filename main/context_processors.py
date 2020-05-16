from main import models


def get_viewed_products(request):
    bucket = request.session.get('bucket', [])
    viewed = []
    for slug in bucket:
        viewed.append(models.Product.objects.get(slug=slug))
    return {'viewed': viewed}