from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    path('',views.ThreadListView.as_view(),name="listThreads"),
    path('post/', views.ThreadPostView.as_view(),name="postThread"),
    path('detail/<str:pk>/',views.ThreadDetailView.as_view(),name="detailThread"),
    path('delete/<str:pk>/',views.ThreadDeleteView.as_view(),name="deleteThread"),
    path('update/<str:pk>/',views.ThreadUpdateTitleView.as_view(), name="updateThread"),
    path('add/<str:pk>/messages/', views.ThreadAddMessage.as_view(), name='add-message-to-thread'),  # Add a message to a thread
    path('update/<str:pk>/messages/<str:message_id>/', views.ThreadUpdateMessage.as_view(), name='update-message-to-thread'),  # Update a message
    path('delete/<str:pk>/messages/<str:message_id>/', views.ThreadDeleteMessage.as_view(), name='delete-message-to-thread'),  # Delete a messag

    
    
]