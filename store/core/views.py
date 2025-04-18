from itertools import product
from os import remove
from urllib import request
from . import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from core.models import Product
from . import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
import json
import requests
from django.contrib.sites.shortcuts import get_current_site


mid = '40120a7a-b6e4-44cb-b9c5-2755e1cb3dab'
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
    def get(self, request):
        form = forms.InvoiceForm()
        return render(request, 'core/checkout.html', {'form': form })

    def post(self, request):
        form = forms.InvoiceForm(request.POST)
        if form.is_valid():

            address_data = {
                'user': request.user,
                'street': request.POST.get('street', ''),
                'city': request.POST.get('city', ''),
                'postal_code': request.POST.get('postal_code', ''),
                'country': request.POST.get('country', ''),
            }

            address, created = models.Address.objects.update_or_create(
                user=request.user,
                defaults=address_data
            )


            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.address = address
            cart = get_cart(request)
            invoice.total_before_discount_in_invoice = get_cart_total_price(cart)
            invoice.save()

            item_objects = []
            items = models.Product.objects.filter(id__in=list(cart.keys()))
            for product_id, product_count in cart.items():
                obj = items.get(id=product_id)
                total_price = obj.price * product_count
                total_price -= total_price * obj.discount

                invoice_item = models.InvoiceItem(
                    product=obj,
                    invoice=invoice,
                    count=product_count,
                    price=obj.price,
                    discount=obj.discount,
                    name=obj.name,
                    total_price_count=total_price
                )
                item_objects.append(invoice_item)
            models.InvoiceItem.objects.bulk_create(item_objects)


            payment = models.Payment()
            payment.invoice = invoice
            payment.total_price = invoice.total_before_discount_in_invoice
            payment.total_price += payment.total_price * invoice.vat
            payment.total_price = int(payment.total_price)
            payment.user_ip = get_user_ip(request)
            payment.description = "Your trusted luxury site"
            payment.save()


            callback_url = f"http://{get_current_site(request)}{reverse('core:verify')}"
            data = {
                "merchant_id": mid,
                "amount": payment.total_price,
                "callback_url": callback_url,
                "description": payment.description,
                "metadata": {
                    "mobile": invoice.user.phone_number,
                    "email": invoice.user.email,
                }
            }

            url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = requests.post(url, data=json.dumps(data), headers=headers)
            response_data = response.json()

            if response_data.get('data', {}).get('code') == 100:
                authority = response_data['data']['authority']
                return redirect(f"https://sandbox.zarinpal.com/pg/StartPay/{authority}")
            else:
                error_message = response_data.get('errors', {}).get('message', 'Unknown error occurred')
                return render(request, 'core/checkout_error.html', {'error_message': error_message})

        return render(request, 'core/checkout.html', {'form': form})


#*********************************************************************************************************
def get_user_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR ')
    if not ip:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#*********************************************************************************************************
class VerifyView(View):
    def get(self, request):
        status = request.GET.get('Status')
        authority = request.GET.get('Authority')
        if status != 'OK':
            return render(request, 'core/payment_failed.html')
        try:
            payment = models.Payment.objects.get(models.Payment, authority=authority , status=models.Payment.STATUS_PENDING)
            amount = payment.total_price
            data = {
                "merchant_id": mid,
                "amount": amount,
                "authority": authority
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            url = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'

            response = requests.post(url, data=json.dumps(data), headers=headers)
            response_data = response.json()
            import logging
            logger = logging.getLogger(__name__)


            if response.status_code == 200:
                code = response_data.get('data', {}).get('code')
                if code == 100:
                    ref_id = str(response_data['data']['ref_id'])
                    payment.ref_id = ref_id
                    payment.status = models.Payment.STATUS_DONE
                    payment.save()
                    return render(request, 'core/payment_done.html')
                elif code == 101:
                    logger.error(f"Failed to pey payment: {json.load(response_data)}")
                    return render(request, 'core/payment_failed.html')
                else:
                    logger.error(f"Failed to pey payment: {json.load(response_data)}")
                    payment.status = models.Payment.STATUS_ERROR
                    payment.save()
                    return render(request, 'core/payment_failed.html')
            else:
                logger.error(f"Failed to pey payment: {json.load(response_data)}")
                payment.status = models.Payment.STATUS_ERROR
                payment.save()
                return render(request, 'core/payment_failed.html')

        except models.Payment.DoesNotExist:
            return render(request, 'core/payment_failed.html')



