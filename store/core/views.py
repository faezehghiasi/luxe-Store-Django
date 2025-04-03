from itertools import product
from os import remove
from urllib import request

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from core.models import Product
from . import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
#*********************************************************************************************************
def get_cart(request):
    cart = request.session.get('cart',{})
    if not cart or not isinstance(cart,dict):
        cart = {}
    return cart
#*********************************************************************************************************
def add_to_cart(cart, product):
    if product.quantity > 0 and product.enabled :
        cart[str(product.id)] = cart.get(str(product.id),0) + 1

#*********************************************************************************************************
def remove_from_cart(cart, product_id):
    if str(product_id) in cart:
        del cart[str(product_id)]

#*********************************************************************************************************

def get_cart_total_price(cart):
   total = 0
   products = models.Product.objects.filter(id__in=list(cart.keys()))

   for product_id , product_count in cart.items():
       obj = products.get(id=product_id)
       total += (obj.price - obj.price * obj.discount) * product_count
   return total
#*********************************************************************************************************
class ListOfProductsView(View):
    def get(self, request):
        #session : { 'cart' : { id : count }}
        list_products =  models.Product.objects.all()
        return render(request,'core/listOfProducts.html',{'list_products':list_products})


#*********************************************************************************************************
class AddToCartView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)
        add_to_cart(cart, product)
        request.session['cart'] = cart

        if request.headers.get('X-Requested-With', '').lower() == 'xmlhttprequest':
            return JsonResponse(cart)
        return HttpResponseRedirect(reverse('core:products_list'))


#*********************************************************************************************************
class RemoveFromView(View):
    def get(self, request, product_id):
        cart = get_cart(request)
        remove_from_cart(cart, product_id)
        request.session['cart'] = cart

        if request.headers.get('X-Requested-With', '').lower() == 'xmlhttprequest':
            return JsonResponse({
                'cart' : cart,
                'total_price' : get_cart_total_price(cart)
            })
        return HttpResponseRedirect(reverse('core:products_list'))

#*********************************************************************************************************
class EmptyCartView(View):
    def get(self, request):
        request.session['cart'] = {}
        if request.headers.get('X-Requested-With', '').lower() == 'xmlhttprequest':
            return JsonResponse({})
        return HttpResponseRedirect(reverse('core:products_list'))

#*********************************************************************************************************
class ShowCartView(View):
    def get(self, request):
        cart = get_cart(request)
        objects = models.Product.objects.filter(id__in=list(cart.keys()))
        cart_objects = {}
        for product_id , product_count in cart.items():
            obj = objects.get(id=product_id)
            cart_objects[product_id] = {
                'obj' :obj ,
                'price':(obj.price - obj.price * obj.discount) * product_count,
                'count' : product_count }

        return render(request,'core/cart.html',{'cart':cart_objects , 'total_price':get_cart_total_price(cart)})

#*********************************************************************************************************
class CheckoutView(View):
    pass

#*********************************************************************************************************