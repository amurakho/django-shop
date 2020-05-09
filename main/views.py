from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic
from django.http import Http404
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from main import models, forms


class ProductList(generic.ListView):
    model = models.Product
    template_name = 'main/product_list.html'
    context_object_name = 'products'
    ordering = 'mean_review'


def filter_view(request):
    if request.is_ajax() and request.method == 'GET':
        orderby = request.GET.get('sort')
        categories = request.GET.getlist('categories')
        search_value = request.GET.get('search_value')

        # todo: by name?
        # todo: подключить другую базу, тогда icontains будет работать
        if categories:
            data = models.Product.objects.filter(category__slug__in=categories, name__icontains=search_value).order_by(orderby)
        else:
            data = models.Product.objects.filter(name__icontains=search_value).order_by(orderby)

        context = {'products': data}
        html_rendered = render_to_string('main/products_for_ajax.html', context)
        return JsonResponse({'html': html_rendered})


class ProductDetail(generic.DetailView):
    model = models.Product
    template_name = 'main/product_detail.html'
    context_object_name = 'product'
    comment_form = forms.ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.comment_form(initial={'rating': '4'})
        return context

    def post(self, request, *args, **kwargs):
        form = self.comment_form(request.POST)
        obj = self.get_object()
        if form.is_valid():
            form.instance.product = obj
            order_id = form.cleaned_data['order_number']
            form.instance.order = models.Order.objects.get(id=order_id)
            form.save()
        return redirect(reverse('product_detail', args=[obj.slug]))


class SearchView(generic.ListView):
    model = models.Product
    template_name = 'main/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('value')
        # todo: Поиск только по имени?
        # todo: подключить другую базу, тогда icontains будет работать
        queryset = models.Product.objects.filter(name__icontains=search_value)
        context['products'] = queryset
        context['search_value'] = search_value
        return context


# @csrf_exempt
# def add_comment(request, slug):
#     if not request.POST or not request.is_ajax():
#         print(request.is_ajax())
#         raise Http404
#
#     order_id = request.POST.get('order_id')
#     order = models.Order.objects.filter(id=order_id)
#
#     if not order:
#         response = JsonResponse({"error": "К сожалению мы не смогли найти Ваш заказ."})
#         response.status_code = 403
#         return response
#
#     product = get_object_or_404(models.Product, slug=slug)
#     comment = models.Review.objects.create(rating=int(request.POST.get('rating')),
#                                            order=order[0],
#                                            text=request.POST.get('text'),
#                                            author=request.POST.get('name'),
#                                            product=product
#                                            )
#     data = {
#         'rating': comment.rating,
#         'text': comment.text,
#         'author': comment.author,
#         'data': comment.date,
#     }
#     return JsonResponse(data)