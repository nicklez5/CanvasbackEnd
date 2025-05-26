from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
urlpatterns = [
    path('detail/<str:pk>/',views.CanvasView.as_view()),
    path('courses/<str:pk>/', views.CanvasCourse.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)