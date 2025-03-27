from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from core.models import Product


class HelloworldView(View):
    def get(self, request):
        return render(request,'helloworld.html')


class ListProductsView(View):
    def get(self, request):

        list_products = Product.objects.all()

        return render(request,'listOfProducts.html',{'list_products':list_products})






