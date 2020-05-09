from django.shortcuts import render, get_object_or_404, redirect, reverse, Http404
from django.views import generic
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from main import models as product_models
from basket import forms


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


class CreateOrder(generic.CreateView):
    form_class = forms.OrderCreationForm
    template_name = 'basket/order_creation.html'
    model = product_models.Order
    success_url = '/'

    def form_valid(self, form):
        bucket_id = self.request.POST.get('bucket')
        bucket = get_object_or_404(product_models.Bucket, id=bucket_id)
        bucket.make_hidden()
        form.instance.bucket = bucket
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_key = self.request.session.session_key
        bucket = get_object_or_404(product_models.Bucket, session_key=session_key)
        context['bucket'] = bucket
        return context