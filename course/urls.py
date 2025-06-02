from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns 
from .views import StudentAllGradesView,StudentAssignmentGradesView,StudentTestGradesView,CourseStudentsView,CourseListView,CoursePostView,CourseDetailView,CourseUpdateView,CourseDeleteView,CourseLecturesView,CourseAssignmentsView,CourseTestsView,CourseThreadsView


urlpatterns = [
    path('', CourseListView.as_view(),name="CourseList"),
    path('post/', CoursePostView.as_view(),name="CoursePost"),
    path('detail/<str:pk>/', CourseDetailView.as_view(),name="CourseDetail"),
    path('update/<str:pk>/', CourseUpdateView.as_view(),name="CourseUpdate"),
    path('delete/<str:pk>/', CourseDeleteView.as_view(),name="CourseDelete"),
    path('lectures/<str:pk>/', CourseLecturesView.as_view(), name="CourseLectures"),
    path('assignments/<str:pk>/', CourseAssignmentsView.as_view(), name="CourseAssignments"),
    path('tests/<str:pk>/', CourseTestsView.as_view(), name="CourseTests"),
    path('threads/<str:pk>/', CourseThreadsView.as_view(), name="CourseThreads"),
    path('<str:course_id>/remove_student/<str:student_id>/', CourseStudentsView.as_view(),name="CourseStudents"),
    path('<str:course_id>/tests/grades/<str:student_id>/',StudentTestGradesView.as_view(),name="StudentTestGrades"),
    path('<str:course_id>/assignments/grades/<str:student_id>/',StudentAssignmentGradesView.as_view(),name="StudentAssignmentGrades"),
    path('<str:course_id>/grades/<str:student_id>/', StudentAllGradesView.as_view(),name="StudentGrades" )
]