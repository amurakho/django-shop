from django.shortcuts import render, get_object_or_404, redirect, reverse, Http404
from django.views import generic
import random

from main import models as product_models


def add_to_bucket(request):
    product_slug = request.POST.get('product')
    if not request.POST or not product_slug:
        return Http404

    session_key = request.session.get('bucket', [])
    bucket, created = product_models.Bucket.objects.get_or_create(session_key=session_key)
    if created:
        request.session['bucket'] = bucket.id
        bucket.save()

    product_in_bucket = bucket.products.filter(product__slug=product_slug)
    if created or not product_in_bucket:
        product = get_object_or_404(product_models.Product, slug=product_slug)
        new_product_in_bucket = product_models.ProductInBucket.objects.create(product=product,
                                                                              count=request.POST.get('count'))
        new_product_in_bucket.save()
        bucket.products.add(new_product_in_bucket)
    elif product_in_bucket:
        product_in_bucket[0].count += int(request.POST.get('count'))
        product_in_bucket[0].save()

    return redirect(reverse('product_detail', args=[product_slug]))
    # return redirect('/')
#
# class GetFromBucket(generic.ListView):
#     model = product_models.Bucket
#     template_name = ''
#     context_object_name = 'products_in_bucket'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         session_key = self.request.session.get('bucket', [])
#         if not session_key