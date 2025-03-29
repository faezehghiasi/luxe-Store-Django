from django.shortcuts import render
from django.views import View
from . import forms
class SignUpView(View):
    def get(self,request):
        form = forms.SignUpForm()
        return render(request,'account/signup.html',{'form':form})

    def post(self,request):
        pass

