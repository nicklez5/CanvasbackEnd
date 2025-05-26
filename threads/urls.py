from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from views import ThreadDetailView,ThreadPostView,ThreadDeleteView,ThreadListView,ThreadMessageCreateView,ThreadMessageUpdateView,ThreadMessageDeleteView
urlpatterns = [
    path('',ThreadListView.as_view()),
    path('post/', ThreadPostView.as_view()),
    path('detail/<str:pk>/',ThreadDetailView.as_view()),
    path('delete/<str:pk>/',ThreadDeleteView.as_view()),
    path('<str:pk>/messages/', ThreadMessageCreateView.as_view(), name='add-message-to-thread'),  # Add a message to a thread
    path('<str:pk>/messages/<str:message_id>/', ThreadMessageUpdateView.as_view(), name='update-message-to-thread'),  # Update a message
    path('<str:pk>/messages/<str:message_id>/delete/', ThreadMessageDeleteView.as_view(), name='delete-message-to-thread'),  # Delete a messag

    
    
]