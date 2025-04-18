from django.shortcuts import render
from django.views import View
from . import forms,models
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from store import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import User
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
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)
#*********************************************************************************************************
activation_token_generator = TokenGenerator()
class SignUpView(View):
    def get(self,request):
        form = forms.SignUpForm()
        return render(request,'account/signup.html',{'form':form})

    def post(self, request):
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            # Save user with inactive status
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Prepare verification email
            mail_subject = 'Activate your LUXE account'

            # Generate activation token and link
            token = activation_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            domain = get_current_site(request)
            activation_url = reverse('account:activate', kwargs={'uid': uid, 'token': token})
            activation_link = f'http://{domain}{activation_url}'


            # Render email content from template
            email_body = render_to_string('account/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            # Create and send email
            email = EmailMessage(
                mail_subject,
                email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.content_subtype = "html"
            try:
                email.send(fail_silently=False)
                return render(request, 'account/signup_done.html', {'user': user})
            except Exception as e:
                # Log the error and show message to user
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to send activation email: {str(e)}")
                form.add_error(None, "Failed to send activation email. Please try again later.")
                user.delete()

                return render(request, 'account/signup.html', {'form': form})

        # Form is invalid - return with errors
        return render(request, 'account/signup.html', {'form': form})
#*********************************************************************************************************
class ActivateView(View):
    def get(self, request, uid, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user_id_int = int(user_id)
        except (TypeError, ValueError, UnicodeDecodeError) as e:
            return render(request, 'account/activation_error.html', {'error': 'Invalid user ID format'})

        try:
            user = models.User.objects.get(pk=user_id_int)
            if user.is_active:
                return render(request, 'account/activation_error.html', {'error': 'user is already active'})
        except models.User.DoesNotExist:
            return render(request, 'account/activation_error.html', {'error': 'User not found'})

        if activation_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, "account/activation_done.html")

        return render(request, 'account/activation_error.html', {'error': 'Invalid token'})

#*********************************************************************************************************
