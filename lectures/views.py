from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .models import Lecture
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from rest_framework import serializers, status 
from .serializers import SerializeLecture 
class LectureList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        lectures = Lecture.objects.all()
        serializer = SerializeLecture(lectures, many=True)
        return Response(serializer.data)

class LecturePost(APIView):
    permission_classes = [IsAdminUser]
    parser_classes=[MultiPartParser]
    def post(self, request, format=None):
        data = request.data
        
        uploaded_file = request.FILES['file']
        if(uploaded_file):
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
        lecture = Lecture.objects.create(name=data.get("name"), description=data.get("description"), file=uploaded_file)
        serializer = SerializeLecture(lecture)
        return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LectureDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            return Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            raise Http404
    
    def get(self, request, pk , format = None):
        lecture = self.get_object(pk)
        serializer = SerializeLecture(lecture)
        return Response(serializer.data)

class LectureUpdate(APIView):
    permission_classes = [IsAdminUser]
    parser_classes= [MultiPartParser]
    def get_object(self,pk):
        try:
            return Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            raise Http404

    def post(self,request,pk,format=None):
        data = request.data
        lecture = self.get_object(pk)
        uploaded_file = request.FILES['file']
        if(uploaded_file):
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
        lecture.description = data.get("description")
        lecture.name = data.get("name")
        lecture.file = uploaded_file
        lecture.save()
        serializer = SerializeLecture(lecture)
        return Response(serializer.data)
        
class LectureDelete(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self,pk):
        try:
            return Lecture.objects.get(pk=pk)
        except Lecture.DoesNotExist:
            raise Http404
            
    def delete(self, request, pk, format=None):
        lecture = self.get_object(pk)
        lecture.delete()
        return Response(status=status.HTTP_200_OK)


# Create your views here.