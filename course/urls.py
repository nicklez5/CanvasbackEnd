from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns 
from . import views 


urlpatterns = [
    path('', views.CourseList,name="CourseList"),
    path('post/', views.CoursePost,name="CoursePost"),
    path('detail/<str:pk>/', views.CourseDetail,name="CourseDetail"),
    path('update/<str:pk>/', views.CourseName,name="CourseName"),
    path('lecture/<str:pk>/', views.CourseLecture, name="CourseLecture"),
    path('assignment/<str:pk>/',views.CourseAssignment,name="CourseAssignment"),
    path('student/<str:pk>/',views.CourseStudent,name="CourseStudent"), 
    path('test/<str:pk>/',views.CourseTest, name="CourseTest"),
    path('thread/<str:pk>/',views.CourseThreads,name="CourseThread"),
    path('edit/<str:pk>/',views.CourseName,name="CourseEdit")
]