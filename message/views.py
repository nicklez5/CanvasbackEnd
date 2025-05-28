from django.shortcuts import render
from .models import Message
from threads.models import Thread
from users.models import CustomUser
from profiles.models import Profile 
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework import serializers, status
from threads.serializers import SerializeThread
from .serializers import SerializeMessage
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.exceptions import PermissionDenied
class MessageList(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = SerializeMessage
    permission_classes = [IsAuthenticated]

class MessagePost(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        # Copy the incoming data to prevent modifying the original request.data
        data = request.data.copy()

        # Set the 'author' field to the authenticated user (User instance, not just user.id)
        data['author'] = request.user  # Set the actual User object, not just the ID

        # Serialize the data
        serializer = SerializeMessage(data=data)

        # Validate and save the message
        if serializer.is_valid():
            serializer.save()  # This will automatically associate the 'author' with the authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class MessageDetailView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = SerializeMessage
    permission_classes = [IsAuthenticated]

class MessageUpdateView(UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = SerializeMessage
    permission_classes = [IsAuthenticated]
    def get_object(self):
        # Retrieve the message based on the primary key (pk)
        message = super().get_object()
        # Ensure that only the author of the message can update it
        if message.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this message.")
        return message
    
class MessageDeleteView(DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = SerializeMessage
    permission_classes = [IsAuthenticated]
    def get_object(self):
        # Retrieve the message based on pk
        message = super().get_object()
        # Ensure that only the author of the message can delete it
        if message.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this message.")
        return message


    
# Create your views here.