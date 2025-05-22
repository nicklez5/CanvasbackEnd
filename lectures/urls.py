from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns 
from . import views
urlpatterns = [
    path('',views.LectureList.as_view()),
    path('post/',views.LecturePost.as_view()),
    path('detail/<str:pk>/', views.LectureDetail.as_view()),
    path('update/<str:pk>/', views.LectureUpdate.as_view()),
    path('delete/<str:pk>/', views.LectureDelete.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)