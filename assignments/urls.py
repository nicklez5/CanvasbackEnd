from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.AssignmentListView.as_view(), name="list"),
    path('post/', views.AssignmentPostView.as_view(), name="create"),
    path('detail/<str:pk>/',views.AssignmentDetail.as_view(), name="detail"),
    path('update/<str:pk>/', views.AssignmentUpdate.as_view(), name="update"),
    path('delete/<str:pk>/', views.AssignmentDelete.as_view(), name="delete"),
]

urlpatterns = format_suffix_patterns(urlpatterns)