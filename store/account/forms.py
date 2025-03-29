from django import forms
from django.core import validators
from phonenumber_field.formfields import PhoneNumberField

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=255,widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=255,widget=forms.PasswordInput)
    #phone_number = forms.CharField(max_length=15,widget=forms.NumberInput,validators=[validators.RegexValidator(r'^(\+98|09|9)?9\d{8}$')])
    phone_number = PhoneNumberField()




