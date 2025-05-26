from django.shortcuts import render

from users.models import CustomUser
from profiles.models import Profile 
from .models import Thread
from django.http import Http404
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, viewsets 
from message.serializers import SerializeMessage
from .serializers import SerializeThread
from .models import Thread
from course.models import Course
from message.models import Message
from django.shortcuts import get_object_or_404

class ThreadListView(ListAPIView):
    queryset = Thread.objects.all()
    serializer_class = SerializeThread
    permission_classes = [IsAuthenticated]

class ThreadDetailView(RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = SerializeThread
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class ThreadPostView(CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = SerializeThread
    permission_classes = [IsAuthenticated]
    
class ThreadDeleteView(DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = SerializeThread
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'
    

class ThreadMessageCreateView(APIView):
    def post(self, request, pk, format=None):
        thread = get_object_or_404(Thread, pk=pk)
        data = request.data
        # Create the message and add to the thread
        msg = Message.objects.create(
            author=data['author'],
            description=data['description'],
            thread=thread
        )
        return Response({"detail": "Message added successfully."}, status=status.HTTP_201_CREATED)
class ThreadMessageUpdateView(APIView):
    def put(self, request, pk, message_id,format=None):
        """
        Update an existing message in the thread.
        """
        thread = get_object_or_404(Thread, pk=pk)

        # Retrieve the message to update
        msg = get_object_or_404(Message, pk=message_id,thread=thread)
        data = request.data
        msg.description = data.get('description', msg.description)
        msg.save()
        # Ensure the message belongs to the thread
        return Response({"detail": "Message updated successfully."}, status=status.HTTP_200_OK)

class ThreadMessageDeleteView(APIView):
    def delete(self, request, pk, message_id, format=None):
        thread = get_object_or_404(Thread, pk=pk)
        msg = get_object_or_404(Message, pk=message_id, thread=thread)
        msg.delete()
        return Response({"detail": "Message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        
