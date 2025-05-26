from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns 
from .views import CourseListView,CoursePostView,CourseDetailView,CourseUpdateView,CourseDeleteView


urlpatterns = [
    path('', CourseListView.as_view(),name="CourseList"),
    path('post/', CoursePostView.as_view(),name="CoursePost"),
    path('detail/<str:pk>/', CourseDetailView.as_view(),name="CourseDetail"),
    path('update/<str:pk>/', CourseUpdateView.as_view(),name="CourseUpdate"),
    path('delete/<str:pk>/', CourseDeleteView.as_view(),name="CourseDelete"),
]