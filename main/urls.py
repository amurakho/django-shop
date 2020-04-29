from django.urls import path, include


from main import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('product/<slug:slug>', views.ProductDetail.as_view(), name='product_detail'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('filter/', views.filter_view, name='filter')
]
