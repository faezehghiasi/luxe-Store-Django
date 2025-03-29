from django.shortcuts import render
from django.views import View
from . import forms

#*********************************************************************************************************
# class SignUpView(View):
#     def get(self,request):
#         form = forms.SignUpForm()
#         return render(request,'account/signup.html',{'form':form})
#
#     def post(self,request):
#         form = forms.SignUpForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data.get('email'))
#
#         return render(request, 'account/signup.html', {'form': form})

#*********************************************************************************************************

class SignUpView(View):
    def get(self,request):
        form = forms.SignUpForm()
        return render(request,'account/signup.html',{'form':form})

    def post(self,request):
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            ...

        return render(request, 'account/signup.html', {'form': form})
#*********************************************************************************************************