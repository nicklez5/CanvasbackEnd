from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.AssignmentListView.as_view(), name="list"),
    path('post/', views.AssignmentPostView.as_view(), name="create"),
    path('detail/<str:pk>/',views.AssignmentDetail.as_view(), name="detail"),
    path('update/<str:pk>/', views.AssignmentUpdate.as_view(), name="update"),
    path('delete/<str:pk>/', views.AssignmentDelete.as_view(), name="delete"),
    path('<str:assignment_id>/submit/', views.AssignmentSubmissionCreateView.as_view(), name="submit"),
    path('<str:assignment_id>/submissions/',views.AssignmentSubmissionListView.as_view(), name="submissions_list"),
    path('submissions/<str:pk>/',views.AssignmentSubmissionDetailView.as_view(), name="submissions"),

]

urlpatterns = format_suffix_patterns(urlpatterns)