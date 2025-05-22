from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.api_assignment_list, name="list"),
    path('post/', views.api_create_assignment, name="create"),
    path('detail/<str:pk>/',views.api_detail_assignment_view, name="detail"),
    path('update/<str:pk>/', views.api_update_assignment_view, name="update"),
    path('delete/<str:pk>/', views.api_delete_assignment, name="delete"),
]

urlpatterns = format_suffix_patterns(urlpatterns)