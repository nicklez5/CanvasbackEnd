from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status 
from .serializers import SerializeProfile
from .models import Profile

class ProfileList(APIView):
    serializer_class = SerializeProfile
    permission_classes = [IsAuthenticated]

    def get(self,request):
        queryset = Profile.objects.all()
        serializer = SerializeProfile(queryset, many=True)
        return Response(serializer.data)
    
    
class ProfileView(APIView):

    serializer_class = SerializeProfile 
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        
    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = SerializeProfile(profile)
        return Response(serializer.data)

class ProfileUpdate(APIView):

    serializer_class = SerializeProfile
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def put(self,request,pk,format=None):
        data = request.data
        profile = self.get_object(pk)
        profile.first_name = data["first_name"]
        profile.last_name = data["last_name"]
        profile.date_of_birth = data["date_of_birth"]
        profile.save()
        serializer = SerializeProfile(profile)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    

# Create your views here.