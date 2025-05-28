from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns 
from .views import CourseListView,CoursePostView,CourseDetailView,CourseUpdateView,CourseDeleteView,CourseLecturesView,CourseProfilesView,CourseAssignmentsView,CourseTestsView,CourseThreadsView


urlpatterns = [
    path('', CourseListView.as_view(),name="CourseList"),
    path('post/', CoursePostView.as_view(),name="CoursePost"),
    path('detail/<str:pk>/', CourseDetailView.as_view(),name="CourseDetail"),
    path('update/<str:pk>/', CourseUpdateView.as_view(),name="CourseUpdate"),
    path('delete/<str:pk>/', CourseDeleteView.as_view(),name="CourseDelete"),
    path('lectures/<str:pk>/', CourseLecturesView.as_view(), name="CourseLectures"),
    path('assignments/<str:pk>/', CourseAssignmentsView.as_view(), name="CourseAssignments"),
    path('tests/<str:pk>/', CourseTestsView.as_view(), name="CourseTests"),
    path('profiles/<str:pk>/', CourseProfilesView.as_view(), name="CourseProfiles"),
    path('threads/<str:pk>/', CourseThreadsView.as_view(), name="CourseThreads"),

]