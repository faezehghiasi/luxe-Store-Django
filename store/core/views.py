from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from core.models import Product
from . import models
from django.http import HttpResponseRedirect
from django.urls import reverse
#*********************************************************************************************************
class ListOfProductsView(View):
    def get(self, request):

        list_products =  models.Product.objects.all()

        return render(request,'core/listOfProducts.html',{'list_products':list_products})


#*********************************************************************************************************
class AddToCartView(View):
    def get(self, request,product_id):
        if not request.session.get('cart'):
            request.session['cart'] = []
        request.session['cart'] = request.session['cart'].append(product_id)
        return HttpResponseRedirect(reverse('core:listOfProducts'))


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