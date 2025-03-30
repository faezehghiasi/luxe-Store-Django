from django import forms
from django.core import validators
from phonenumber_field.formfields import PhoneNumberField
from . import models
from django.contrib.auth.forms import UserCreationForm


#*********************************************************************************************************
# class SignUpForm(forms.Form):
#     first_name = forms.CharField(max_length=255)
#     last_name = forms.CharField(max_length=255)
#     email = forms.EmailField()
#     password1 = forms.CharField(max_length=255,widget=forms.PasswordInput)
#     password2 = forms.CharField(max_length=255,widget=forms.PasswordInput)
#     #phone_number = forms.CharField(max_length=15,widget=forms.NumberInput,validators=[validators.RegexValidator(r'^(\+98|09|9)?9\d{8}$')])
#     phone_number = PhoneNumberField()
#
#*********************************************************************************************************

class SignUpForm(UserCreationForm):
    class Meta:
        model = models.User
        exclude = ['is_staff', 'is_superuser', 'is_active', 'date_joined', 'groups', 'user_permissions','last_login','avatar','address','password']
        # fields = ['first_name', 'last_name', 'email','phone_number','password']
        # fields = '__all__'


# *********************************************************************************************************

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2