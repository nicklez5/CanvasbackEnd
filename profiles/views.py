from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.generics import RetrieveAPIView,ListAPIView,UpdateAPIView
from .serializers import SerializeProfile
from .models import Profile
from course.models import Course
class ProfileListView(APIView):
    serializer_class = SerializeProfile
    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset = Profile.objects.all()
        serializer = SerializeProfile(queryset, many=True)
        return Response(serializer.data)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self):
        # Always return the Profile for the currently authenticated user
        return self.request.user.profile

    def get(self, request, *args, **kwargs):
        # Retrieve the profile of the authenticated user
        profile = request.user.profile  # Access the profile via the reverse relationship (user.profile)
        
        # Serialize the profile data
        serializer = SerializeProfile(profile)
        
        # Return the serialized data as a response
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # Retrieve the profile of the authenticated user
        profile = request.user.profile
        
        # Serialize the updated data
        serializer = SerializeProfile(profile, data=request.data, partial=True)  # partial=True for partial updates
        
        if serializer.is_valid():
            new_profile = serializer.save()
            courses = Course.objects.filter(profiles__id=request.user.id)
            for course in courses:
                course.profiles.filter(id=request.user.id).update(first_name=new_profile.first_name, last_name=new_profile.last_name, date_of_birth=new_profile.date_of_birth)
              # Save the updated profile data
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
        

    

# Create your views here.