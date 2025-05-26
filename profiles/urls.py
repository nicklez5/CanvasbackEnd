from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from . import views 
urlpatterns = [
    path('', views.ProfileListView.as_view()),
    path('<str:pk>/', views.ProfileView.as_view()),
    path('update/<str:pk>/', views.ProfileUpdateView.as_view()),
]