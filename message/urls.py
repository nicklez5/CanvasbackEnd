from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    path('',views.MessageList.as_view()),
    path('post/',views.MessagePost.as_view()),
    path('detail/<str:pk>/',views.MessageDetail.as_view()),
    path('update/<str:pk>/',views.MessageUpdate.as_view()),
    path('delete/<str:pk>/',views.MessageDelete.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)