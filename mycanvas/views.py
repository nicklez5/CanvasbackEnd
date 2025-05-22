from django.shortcuts import render, redirect 
from rest_framework.decorators import action, permission_classes 
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response 
from rest_framework import status, viewsets
from course.serializers import SerializeCourse
from .serializers import SerializeCanvas
from .models import Canvas 
from course.models import Course
 
class CanvasList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SerializeCanvas
    parser_classes=[MultiPartParser]
    def get(self,request,format=None):
        canvas = Canvas.objects.all()
        serializer = self.serializer_class(canvas,many=True)
        return Response(serializer.data)

    
class CanvasView(APIView):
    serializer_class = SerializeCanvas
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Canvas.objects.get(pk=pk)
        except Canvas.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def get(self, request , pk , format=None):
        canvas = self.get_object(pk)
        serializer = SerializeCanvas(canvas)
        return Response(serializer.data)


class CanvasRemoveCourse(APIView):
   
    serializer_class = SerializeCanvas
    permission_classes = [IsAdminUser]

    def get_object(self,pk):
        try:
            return Canvas.objects.get(pk=pk)
        except Canvas.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def put(self,request,pk,format=None):
        data = request.data
        canvas = self.get_object(pk)
        course_ID = data['id']
        try:
            course = Course.objects.get(pk=course_ID)
            canvas.list_courses.remove(course)
            canvas.save()
        except Course.DoesNotExist:
            print("Course Does not exist")

        serializer = self.serializer_class(canvas)
        return Response(serializer.data)


class CanvasAddCourse(APIView):
    serializer_class = SerializeCanvas
    permission_classes = [IsAdminUser]

    def get_object(self,pk):
        try:
            return Canvas.objects.get(pk=pk)
        except Canvas.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def put(self,request,pk,format=None):
        data = request.data
        canvas = self.get_object(pk)
        course_ID = data['id']

        try:
            course = Course.objects.get(pk=int(course_ID))
            canvas.list_courses.add(course)
            canvas.save()
        except Course.DoesNotExist:
            print("Course Does not exist")
        
        serializer = SerializeCanvas(canvas)
        return Response(serializer.data)
        



