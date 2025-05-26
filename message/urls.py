from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    path('',views.MessageList.as_view()),
    path('post/',views.MessageCreateView.as_view()),
    path('detail/<str:pk>/',views.MessageDetailView.as_view()),
    path('update/<str:pk>/',views.MessageUpdateView.as_view()),
    path('delete/<str:pk>/',views.MessageDeleteView.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)