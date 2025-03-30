
from django.urls import path, include,re_path
from . import views
urlpatterns = [

    path('signup/', views.SignUpView.as_view(), name='signup'),

]