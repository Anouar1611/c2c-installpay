from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('make_payment/<int:plan_id>/', views.make_payment, name='make_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
]
