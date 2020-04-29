from django.urls import path

from bucket import views

urlpatterns = [
    # path('', views.GetFromBucket.as_view(), name='bucket'),
    path('add/', views.add_to_bucket, name='to_bucket'),
]
