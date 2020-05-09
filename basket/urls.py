from django.urls import path

from basket import views

urlpatterns = [
    # path('', views.GetFromBucket.as_view(), name='basket'),
    path('add/', views.add_to_bucket, name='to_bucket'),
    path('order/', views.CreateOrder.as_view(), name='order_creation'),
]
