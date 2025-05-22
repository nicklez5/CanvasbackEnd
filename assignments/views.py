from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from .models import Assignment
from .serializers import SerializeAssignment
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers , status 
from .forms import AssignmentForm
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_assignment_list(request):
    if request.method == 'GET':
        assignments = Assignment.objects.all()
        serializer = SerializeAssignment(assignments, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def api_create_assignment(request):
    
    if request.method == 'POST':
        data = request.data
        uploaded_file = request.FILES["file"]
        if(uploaded_file):
            fs = FileSystemStorage()
            fs.save(uploaded_file.name,uploaded_file)

        assignment_name = data["name"]
        assignment_submitter = data["submitter"]
        assignment_date_due = data["date_due"]
        assignment_max_points = data["max_points"]
        assignment_student_points = data["student_points"]
        assignment_description = data["description"]
        assignment_file = uploaded_file
        assignment = Assignment.objects.create(name=assignment_name, submitter = assignment_submitter, date_due = assignment_date_due, max_points = assignment_max_points, student_points = assignment_student_points, description = assignment_description,file=assignment_file)
        serializer = SerializeAssignment(assignment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_assignment_view(request,pk):
    try:
        assignment_post = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SerializeAssignment(assignment_post)
        return Response(serializer.data)



@api_view([ 'POST', ])
@permission_classes((IsAuthenticated, ))
def api_update_assignment_view(request, pk):
    try:
        assignment_post = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        data = request.data
        uploaded_file = request.FILES["file"]
        if(uploaded_file):
            fs = FileSystemStorage()
            fs.save(uploaded_file.name,uploaded_file)
        assignment_post.name = data["name"]
        assignment_post.submitter = data["submitter"]
        assignment_post.date_due = data["date_due"]
        assignment_post.max_points = data["max_points"]
        assignment_post.student_points = data["student_points"]
        assignment_post.description = data["description"]
        assignment_post.file = uploaded_file
        
        assignment_post.save()
        serializer = SerializeAssignment(assignment_post)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
      
    
@api_view(['DELETE', ])
@permission_classes((IsAdminUser, ))
def api_delete_assignment(request,pk):
    try:
        assignment_post = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        raise Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        operation = assignment_post.delete()
        data = {}
        if operation:
            data['response'] = 'Delete success'
        return Response(data=data)
    

# Create your views here.