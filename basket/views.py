from django.shortcuts import render, get_object_or_404, redirect, reverse, Http404
from django.views import generic
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from main import models as product_models


@csrf_exempt
def add_to_bucket(request):
    product_slug = request.POST.get('product')
    product_count = request.POST.get('count')

    if not request.POST or not product_slug or not request.is_ajax():
        raise Http404

    session_key = request.session.session_key
    bucket, created = product_models.Bucket.objects.get_or_create(session_key=session_key)

    product = get_object_or_404(product_models.Product, slug=product_slug)
    product_in_bucket, created = bucket.products.get_or_create(product=product,
                                                                defaults={'count': product_count})
    if not created:
        product_in_bucket.count += int(product_count)
        product_in_bucket.save()

    products_in_basket = bucket.products.all()
    data = {'products_in_bucket': []}
    count = 0
    for item in products_in_basket:
        item_data = {
            'count': item.count,
            'full_price': item.full_price,
            'name': item.product.name
        }
        count += item.count
        data['products_in_bucket'].append(item_data)
    data['products_number'] = count
    return JsonResponse(data)

    # product_in_bucket = bucket.products.filter(product__slug=product_slug)
    # if created or not product_in_bucket:
    #     product = get_object_or_404(product_models.Product, slug=product_slug)
    #     new_product_in_bucket = product_models.ProductInBucket.objects.create(product=product,
    #                                                                           count=product_count)
    #     bucket.products.add(new_product_in_bucket)
    # else:
    #     product_in_bucket[0].count += int(product_count)
    #     product_in_bucket[0].save()
    #
    # return JsonResponse(product_in_bucket.dict())

    # return redirect(reverse('product_detail', args=[product_slug]))
#
# class GetFromBucket(generic.ListView):
#     model = product_models.Bucket
#     template_name = ''
#     context_object_name = 'products_in_bucket'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         session_key = self.request.session.get('basket', [])
#         if not session_key