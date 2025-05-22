from django.shortcuts import get_object_or_404, render
from django.conf import settings
from rest_framework.decorators import action, permission_classes 
from .models import Course
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import serializers, status, viewsets 
from rest_framework.decorators import api_view, parser_classes, permission_classes
from .serializers import SerializeCourse,SerializeAssignment, SerializeLecture
from lectures.models import Lecture 
from assignments.models import Assignment
from profiles.models import Profile 
from tests.models import Tests
from users.models import CustomUser
from mycanvas.models import Canvas
from threads.models import Thread 
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import json
import django.dispatch 

@api_view(['GET',])
@permission_classes((AllowAny,))
def CourseList(request):
    if request.method == "GET":
        courses = Course.objects.all()
        serializer = SerializeCourse(courses,many=True)
        return Response(serializer.data)


@api_view(['POST',])
@permission_classes((IsAdminUser,))
def CoursePost(request,pk):
    if request.method == "POST":
        data = request.data
        courses = Course.objects.create(name = data.get("name"))
        serializer = SerializeCourse(courses)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def post(self,request,format=None):
    #     serializer = SerializeCourse(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET',])
@permission_classes((AllowAny,))
def CourseDetail(request,pk):
    
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = SerializeCourse(course)
        return Response(serializer.data)

 
@api_view(['PUT',])
@permission_classes((IsAdminUser,))
def CourseName(request,pk):
    
    try:
        course =  Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        data = request.data
        course.name = data["name"]
        
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data)
        

@api_view(['POST','GET','DELETE'])
@permission_classes((IsAdminUser,))
 
def CourseLecture(request,pk):


    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        courselectures = course.lectures
        serializer = SerializeLecture(courselectures, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        
        uploaded_file = request.FILES.get("file")
        if(uploaded_file):
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            
        alldata = request.data
        lecture_id = alldata.get("id")
        try:
            lecture_obj = Lecture.objects.get(pk=lecture_id)
            course.lectures.filter(pk=lecture_id).update(
                name=alldata.get("name"), 
                description=alldata.get("description"),    
                file= uploaded_file)
        except Lecture.DoesNotExist:
            lecture_obj = Lecture.objects.create(name = alldata.get("name"),description = alldata.get("description"),file = uploaded_file)
            course.lectures.add(lecture_obj)
        finally:
            course.save()
            serializer = SerializeCourse(course)
            return Response(serializer.data)
    if request.method == "DELETE":
        data = request.data
        
        lecture_id = data.get("id")
        try:
            lecture_obj = Lecture.objects.get(pk=lecture_id)
            course.lectures.remove(lecture_obj)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        finally:
            course.save()
            serializer = SerializeCourse(course)
            return Response(serializer.data)
        

@api_view(['POST','GET','DELETE'])
@permission_classes((IsAdminUser,))

def CourseAssignment(request,pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        courseAssignments = course.assignments
        serializer = SerializeAssignment(courseAssignments, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        data = request.data
        uploaded_file = request.FILES.get("file")
        if(uploaded_file):
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            
        
        assignment_id = data.get("id")
        assignment_name = data.get("name")
        assignment_submitter = data.get("submitter")
        assignment_description = data.get("description")
        assignment_max_points = data.get("max_points")
        assignment_student_points = data.get("student_points")
        assignment_date = data.get("date_due")
        try:
            assignment_obj = Assignment.objects.get(pk = assignment_id)
            course.assignments.filter(pk=assignment_id).update(
                    name=assignment_name, submitter= assignment_submitter,date_due= assignment_date,
                    description=assignment_description, max_points=assignment_max_points, student_points = assignment_student_points,
                    file= uploaded_file)
        except Assignment.DoesNotExist:
            assignment_obj = Assignment.objects.create(name=assignment_name, submitter= assignment_submitter,date_due= assignment_date,
                    description=assignment_description, max_points=assignment_max_points, student_points = assignment_student_points,
                    file= uploaded_file)
            course.assignments.add(assignment_obj)
        finally:
            course.save()
            serializer = SerializeCourse(course)
            return Response(serializer.data)
    if request.method == "DELETE":
        data = request.data
        
        assignment_id = data.get("id")
        assignment_obj = Assignment.objects.get(pk=assignment_id) 
        if assignment_obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        course.assignments.remove(assignment_obj)
        assignment_obj.delete()
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data)
@api_view(['POST','DELETE'])
@permission_classes((IsAdminUser,))
def CourseStudent(request,pk):

    
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "POST":
        data = request.data
        try:
            user_obj = CustomUser.objects.get(email=data["email"])
        except CustomUser.DoesNotExist:
            user_obj = None
        
        (student_canvas,found) = user_obj.canvas
        if(found):
            student_canvas.list_courses.add(course)
            student_canvas.save()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        (student_profile,found1) = user_obj.profile
        if(found1):
            course.profiles.add(student_profile)
            course.save()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SerializeCourse(course)
        return Response(serializer.data)
    if request.method == "DELETE":
        data = request.data
        try:
            user_obj = CustomUser.objects.get(email=data["email"])
        except CustomUser.DoesNotExist:
            user_obj = None
        (student_canvas,found) = user_obj.canvas
        if(found):
            student_canvas.list_courses.remove(course)
            student_canvas.save()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        (student_profile,found1) = user_obj.profile
        if(found1):
            course.profiles.remove(student_profile)
            course.save()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SerializeCourse(course)
        return Response(serializer.data)

@api_view(['POST','DELETE'])
@permission_classes((IsAdminUser,)) 
def CourseTest(request,pk):

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        if(uploaded_file):
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
        data = request.data
        test_id = data.get("id")
        test_description = data.get("description") 
        test_name = data.get("name") 
        test_submitter = data.get("submitter") 
        test_max_points = data.get("max_points") 
        test_student_points = data.get("student_points") 
        test_date_due = data.get("date_due") 
        test_file = uploaded_file
        try:
            test_obj = Tests.objects.get(pk=test_id)
            course.tests.filter(pk = test_id).update(
                description=test_description, name=test_name,submitter=test_submitter,max_points=test_max_points,student_points=test_student_points,file=test_file
            )
        except Tests.DoesNotExist:
            test_obj = Tests.objects.create(name=test_name,description = test_description, submitter = test_submitter, max_points = test_max_points, student_points = test_student_points, date_due = test_date_due, file = test_file)
            course.tests.add(test_obj)
        finally:
            course.save()
            serializer = SerializeCourse(course)
            return Response(serializer.data)
    
    if request.method == "DELETE":
        data = request.data
        test_id = data.get("id")
        try:
            test_obj = Tests.objects.get(pk=test_id)
        except Tests.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        course.tests.remove(test_obj)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data)
@api_view(['POST','DELETE'])
@permission_classes ((IsAuthenticated,))
def CourseThreads(request,pk):
    
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "POST":
        data = request.data
        thread_id = data["id"]
        try:
            thread_obj = Thread.objects.get(pk=thread_id)
        except Thread.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        course.threads.add(thread_obj)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data)
    if request.method == "DELETE":
        data = request.data
        thread_id = data["id"]
        try:
            thread_obj = Thread.objects.get(pk=thread_id)
        except Thread.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        course.threads.remove(thread_obj)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data)


    




    
        

        

    

# Create your views here.