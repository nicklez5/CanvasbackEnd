from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from .models import Course
from .serializers import SerializeCourse, SerializeLecture, SerializeAssignment, SerializeProfile,SerializeTest,SerializeThread
from django.shortcuts import get_object_or_404
from lectures.models import Lecture 
from assignments.models import Assignment
from profiles.models import Profile 
from tests.models import Tests
from users.models import CustomUser
from mycanvas.models import Canvas
from threads.models import Thread 
from django.core.files.storage import FileSystemStorage

class CourseListView(APIView):
    permission_classes = [AllowAny]
    def get(self,request,format=None):
        """Get all courses"""
        courses = Course.objects.all()
        serializer = SerializeCourse(courses, many=True)
        return Response(serializer.data)


class CoursePostView(APIView):
    permission_classes = [IsAdminUser]  # Optional: Only allow admins to create courses

    def post(self, request, format=None):
        """
        Create a new course.
        """
        data = request.data
        
        # Ensure that the name of the course is provided
        course_name = data.get("name")
        if not course_name:
            return Response({"detail": "Course name is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the course using the provided data
        course = Course.objects.create(name=course_name)
        
        # Optionally: If there are other fields like lectures, assignments, etc. you could add them here

        # Serialize the created course and return it in the response
        serializer = SerializeCourse(course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self,request,pk,format=None):

        """Get details of a specific course"""
        if request.method == "GET":
            course = Course.objects.get(id=pk)
            serializer = SerializeCourse(course)
            return Response(serializer.data)


class CourseDeleteView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can delete courses

    def delete(self, request, pk, format=None):
        """
        Delete a specific course by its pk (primary key).
        """
        # Retrieve the course using the provided primary key (pk)
        course = get_object_or_404(Course, pk=pk)
        
        # Delete the course from the database
        course.delete()
        
        # Return a success response
        return Response({"detail": "Course deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
class CourseUpdateView(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, pk, format=None):
        """
        Update the name of a course by its pk (primary key).
        """
        # Retrieve the course using the provided primary key (pk)
        course = get_object_or_404(Course, pk=pk)

        # Get the data from the request
        data = request.data
        new_name = data.get("name")

        # Ensure that the name field is provided in the request
        if not new_name:
            return Response({"detail": "Course name is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the course name
        course.name = new_name
        course.save()

        # Serialize the updated course and return the response
        serializer = SerializeCourse(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseLecturesView(APIView):
    def get_permissions(self):
        """
        Set different permissions for different HTTP methods.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Allow authenticated users for PUT requests
        return [IsAdminUser()]
    def get(self, request, pk, format=None):
        """Get the details of a specific course."""
        course = get_object_or_404(Course, pk=pk)
        lectures = course.lectures.all()
        serializer = SerializeLecture(lectures, many=True)
        return Response(serializer.data)
    def post(self,request,pk,format=None):
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        lecture_id = data.get("id")
        lecture = get_object_or_404(Lecture, pk=lecture_id)
        course.lectures.add(lecture)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def patch(self,request,pk,format=None):
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        lecture_id = data.get("id")
        lecture = get_object_or_404(Lecture, pk=lecture_id)
        course.lectures.remove(lecture)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        # Fetch the course by its primary key (pk)
        course = get_object_or_404(Course, pk=pk)
        
        # Extract data from the request
        data = request.data
        lecture_id = data.get("id")
        if not lecture_id:
            return Response({"detail": "Lecture ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES.get("file")

        # Fetch the lecture by its ID
        lecture = get_object_or_404(Lecture, pk=lecture_id)

        # Only update the fields that are provided in the request data
        if 'name' in data:
            lecture.name = data.get("name", lecture.name)
        if 'description' in data:
            lecture.description = data.get("description", lecture.description)
        
        # Handle file upload if provided
        if file:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            lecture.file = fs.url(filename)  # Update file URL in the lecture model
        
        # Save the updated lecture
        lecture.save()

        # Return the updated course with the modified lecture
        serializer = SerializeCourse(course)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CourseAssignmentsView(APIView):
    def get_permissions(self):
        """
        Set different permissions for different HTTP methods.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Allow authenticated users for PUT requests
        return [IsAdminUser()]
    def get(self, request, pk, format=None):
        """Get the details of a specific course."""
        course = get_object_or_404(Course, pk=pk)
        assignments = course.assignments.all()
        serializer = SerializeAssignment(assignments, many=True)
        return Response(serializer.data)
    def post(self,request,pk,format=None):
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        assignment_id = data.get("id")
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        course.assignments.add(assignment)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def patch(self,request,pk,format=None):
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        assignment_id = data.get("id")
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        course.assignments.remove(assignment)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        """
        Update the assignments for a specific course.
        """
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        assignment_id = data.get("id")

        if not assignment_id:
            return Response({"detail": "Assignment ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the assignment object by ID
        assignment = get_object_or_404(Assignment, pk=assignment_id)

        # If the assignment is to be updated, modify its fields here
        assignment.name = data.get("name", assignment.name)
        assignment.description = data.get("description", assignment.description)
        assignment.date_due = data.get("date_due", assignment.date_due)
        assignment.max_points = data.get("max_points", assignment.max_points)
        assignment.student_points = data.get("student_points", assignment.student_points)
        
        # Optionally update the file if it has been provided
        file = request.FILES.get("assignment_file")
        if file:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            assignment.assignment_file = file_url  # Update assignment file URL

        # Save the updated assignment
        assignment.save()

        # If you want to add or remove assignments from the course, 
        # you can modify the `assignments` field of the course here.
        # If you want to re-link the updated assignment to the course, do this:
        if assignment not in course.assignments.all():
            course.assignments.add(assignment)  # Add assignment to course if not already there

        course.save()

        # Serialize the updated course data and return the response
        serializer = SerializeAssignment(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseTestsView(APIView):
    def get_permissions(self):
        """
        Set different permissions for different HTTP methods.
        """
        if self.request.method == 'PUT' or self.request.method == 'GET':
            return [IsAuthenticated()]  # Allow authenticated users for PUT requests
        return [IsAdminUser()]
    def get(self, request, pk, format=None):
        """Get the details of a specific course."""
        course = get_object_or_404(Course, pk=pk)
        tests = course.tests.all()
        serializer = SerializeTest(tests, many=True)
        return Response(serializer.data)
    def post(self,request,pk,format=None):
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        test_id = data.get("id")
        test = get_object_or_404(Tests, pk=test_id)
        course.tests.add(test)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def patch(self,request,pk,format=None):
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        test_id = data.get("id")
        test = get_object_or_404(Tests, pk=test_id)
        course.tests.remove(test)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        # Fetch the course by its ID
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        test_id = data.get("id")
        # Fetch the test by its ID
        test = get_object_or_404(Tests, pk=test_id)
        
        # Extract the updated data from the request
        test.name = data.get('name', test.name)
        test.description = data.get('description', test.description)
        test.date_due = data.get('date_due', test.date_due)
        test.max_points = data.get('max_points', test.max_points)
        test.student_points = data.get('student_points', test.student_points)

        # Handle file upload for the test
        file = request.FILES.get('test_file')
        if file:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            test.file = file_url  # Update the test file URL
        
        # Save the updated test
        test.save()

        # Ensure the updated test is linked to the course
        if test not in course.tests.all():
            course.tests.add(test)

        course.save()

        # Serialize the updated course with the modified tests
        serializer = SerializeTest(test)
        return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "You must be authenticated to submit an assignment."}, status=status.HTTP_401_UNAUTHORIZED)

class CourseThreadsView(APIView):
    def get_permissions(self):
        """
        Set different permissions for different HTTP methods.
        """
        if self.request.method == 'PUT' or self.request.method == 'GET':
            return [IsAuthenticated()]  # Allow authenticated users for PUT requests
        return [IsAdminUser()]
    def get(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        threads = course.threads.all()
        serializer = SerializeThread(threads, many=True)
        return Response(serializer.data)
    def post(self,request,pk,format=None):
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        thread_id = data.get("id")
        thread = get_object_or_404(Thread, pk=thread_id)
        course.threads.add(thread)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def patch(self,request,pk,format=None):
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        thread_id = data.get("id")
        thread = get_object_or_404(Thread, pk=thread_id)
        course.threads.remove(thread)
        course.save()
        serializer = SerializeCourse(course)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        course = get_object_or_404(Course, pk=pk)
        data = request.data
        thread_id = data.get("id")
        thread = get_object_or_404(thread, pk=thread_id)
        thread.title = data.get("title", thread.title)
        thread.save()
        serializer = SerializeThread(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CourseStudentsView(APIView):
    permission_classes = [IsAdminUser]
    def post(self,request,course_id,student_id):
        try:
            course = Course.objects.get(id=course_id)
            student = CustomUser.objects.get(id=student_id)
            course.profiles.remove(student.profile)
            student.canvas.list_courses.remove(course)
            course.save()
            return Response({"message": "Student removed from course and canvas updated."}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
    