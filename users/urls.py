from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns 
from rest_framework.authtoken.views import obtain_auth_token 
from . import views 

urlpatterns = [
    path('',views.UserList.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.CustomAuthToken.as_view()),
    path('detail/<str:pk>/', views.UserView.as_view()), 
    path('change_password/<str:pk>/', views.UpdatePassword.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)