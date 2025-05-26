from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.generics import RetrieveAPIView,ListAPIView,UpdateAPIView
from .serializers import SerializeProfile
from .models import Profile

class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = SerializeProfile
    permission_classes = [IsAuthenticated]

    
class ProfileView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = SerializeProfile
    permission_classes = [IsAuthenticated]
    def get_object(self):
        """
        Override to retrieve the profile of the currently authenticated user.
        """
        return self.request.user.profile

class ProfileUpdateView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = SerializeProfile
    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        # Get the Profile instance
        profile = self.get_object()
        
        # Get the associated User object
        

        # Check if email is provided in the request and update the email in the User model
        

        # Continue to update other fields for the profile
        profile.first_name = request.data.get('first_name', profile.first_name)
        profile.last_name = request.data.get('last_name', profile.last_name)
        profile.date_of_birth = request.data.get('date_of_birth', profile.date_of_birth)
        profile.save()

        # Return the updated profile data
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        

    

# Create your views here.