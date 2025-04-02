
from django.contrib import admin
from django.urls import path, include,re_path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.ListOfProductsView.as_view(),name='products_list'),
    path('cart/add/<int:product_id>',views.AddToCartView.as_view(),name='cart_add'),
    path('cart/remove/<int:product_id>',views.RemoveFromView.as_view(),name='cart_remove'),
    path('cart/empty',views.EmptyCartView.as_view(),name='cart_empty'),

    path('cart',views.ShowCartView.as_view(),name='cart_show'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),

]