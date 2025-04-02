from django.shortcuts import render
from django.http import HttpResponse
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
        cart[product.id] = cart.get(product.id,0) + 1

#*********************************************************************************************************
def delete_from_cart(cart, product):
   if product.id in cart:
       del cart[product.id]
#*********************************************************************************************************
class ListOfProductsView(View):
    def get(self, request):
        #session : { 'cart' : { id : count }}
        list_products =  models.Product.objects.all()

        return render(request,'core/listOfProducts.html',{'list_products':list_products})


#*********************************************************************************************************
class AddToCartView(View):
    def get(self, request,product_id):
        product = get_object_or_404(Product,id=product_id)
        cart = get_cart(request)
        add_to_cart(cart,product)
        request.session['cart'] = cart
        return HttpResponseRedirect(reverse('core:products_list'))


#*********************************************************************************************************
class RemoveFromView(View):
    pass

#*********************************************************************************************************
class EmptyCartView(View):
    pass

#*********************************************************************************************************
class ShowCartView(View):
    pass

#*********************************************************************************************************
class CheckoutView(View):
    pass

#*********************************************************************************************************