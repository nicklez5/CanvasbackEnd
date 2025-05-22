from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.api_test_list,name="list"),
    path('post/',views.api_create_test, name="create"),
    path('detail/<str:pk>/',views.api_detail_test_view, name="detail"),
    path('update/<str:pk>/', views.api_update_test_view, name="update"),
    path('delete/<str:pk>/', views.api_delete_test, name="delete")
]

urlpatterns = format_suffix_patterns(urlpatterns)