
from django.urls import path, include,re_path
from . import views

app_name = 'account'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<str:uid>/<str:token>/', views.ActivateView.as_view(), name='activate'),
]