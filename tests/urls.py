from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.TestListView.as_view(),name="list"),
    path('post/',views.TestPostView.as_view(), name="create"),
    path('detail/<str:pk>/',views.TestDetailView.as_view(), name="detail"),
    path('update/<str:pk>/', views.TestUpdateView.as_view(), name="update"),
    path('delete/<str:pk>/', views.TestDeleteView.as_view(), name="delete")
]

urlpatterns = format_suffix_patterns(urlpatterns)