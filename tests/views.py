from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import FileUploadParser, MultiPartParser
from .models import Tests
from .serializers import SerializeTest
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .forms import TestForm

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_test_list(request):
    if request.method == 'GET':
        tests = Tests.objects.all()
        serializers = SerializeTest(tests,many=True)
        return Response(serializers.data)
    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_test(request):
    if request.method == "POST":
        data = request.POST 

        uploaded_file = request.FILES['file']
        if(uploaded_file):
            fs = FileSystemStorage()
            fs.save(uploaded_file.name,uploaded_file)
        file = uploaded_file
        description = data.get("description")
        date_due = data.get("date_due")
        name = data.get("name")
        submitter = data.get("submitter")
        max_points = data.get("max_points")
        student_points = data.get("student_points")
        tests = Tests.objects.create(description= description, date_due = date_due, name = name, submitter= submitter, max_points = max_points,student_points = student_points, file = file)
        serializer = SerializeTest(tests)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_test_view(request,pk):
    try:
        Test_post = Tests.objects.get(pk=pk)
    except Tests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = SerializeTest(Test_post)
        return Response(serializer.data)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_update_test_view(request,pk):
    try:
        test_post = Tests.objects.get(pk=pk)
    except Tests.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        data = request.POST 
        uploaded_file = request.FILES['file']
        test_post.description = data.get("description")
        test_post.date_due = data.get("date_due")
        test_post.name = data.get("name")
        test_post.submitter = data.get("submitter")
        test_post.max_points = data.get("max_points")
        test_post.student_points = data.get("student_points")
        if(uploaded_file):
            fs = FileSystemStorage()
            fs.save(uploaded_file.name,uploaded_file)
            test_post.file = uploaded_file
        test_post.save()
        serializer = SerializeTest(test_post)
        return Response(serializer.data)
        return Response(status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',])
@permission_classes([IsAdminUser,])
def api_delete_test(request,pk):
    try:
        test_post = Tests.objects.get(pk=pk)
    except Tests.DoesNotExist:
        raise Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "DELETE":
        operation = test_post.delete()
        data = {}
        if operation:
            data['response'] = 'Delete success'
        return Response(data=data)
# Create your views here.
