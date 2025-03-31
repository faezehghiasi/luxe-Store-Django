from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from core.models import Product
from . import models

#*********************************************************************************************************
class ListOfProductsView(View):
    def get(self, request):

        list_products =  models.Product.objects.all()

        return render(request,'core/listOfProducts.html',{'list_products':list_products})


#*********************************************************************************************************



