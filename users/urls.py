from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns 
from rest_framework.authtoken.views import obtain_auth_token 
from . import views 

urlpatterns = [
    path('',views.UserList.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.CustomAuthToken.as_view()),
    path('detail/', views.UserView.as_view() ,name="user-detail-update"), 
    path('change-password/', views.ChangePasswordView.as_view(), name="change-password"),
    path('forgot-password/',views.ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/<uidb64>/<token>/',views.ResetPasswordAPIView.as_view(), name='reset-password'),
]

urlpatterns = format_suffix_patterns(urlpatterns)