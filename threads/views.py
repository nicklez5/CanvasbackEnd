from django.shortcuts import render
from message.serializers import SerializeMessage
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
from rest_framework.exceptions import NotFound
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

class ThreadUpdateTitleView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        # Fetch the thread object using the primary key (pk)
        thread = get_object_or_404(Thread, pk=pk)

        # Ensure the authenticated user is the author of the thread or an admin
        if thread.author != request.user:
            return Response({"detail": "You do not have permission to edit this thread."}, status=status.HTTP_403_FORBIDDEN)

        # Get the new title from the request data
        new_title = request.data.get('title', None)

        if not new_title:
            return Response({"detail": "Title is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the thread's title
        thread.title = new_title
        thread.save()

        # Serialize the updated thread to return the updated data
        serializer = SerializeThread(thread)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
class ThreadDeleteView(DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = SerializeThread
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'
    def destroy(self, request, *args, **kwargs):
        # Optionally add custom logic before deletion
        response = super().destroy(request, *args, **kwargs)
        # Optionally modify the response here if needed
        return Response({"message": "Thread successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

class ThreadAddMessage(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        data = request.data
        # Get the Thread object to associate the message with
        thread = get_object_or_404(Thread, pk=pk)
        # Create the message and associate it with the thread
        message = Message.objects.create(
            author=request.user,  # Automatically set the author to the current authenticated user
            body=data['body'],  # Get the body of the message from the request
        )
        # Create the message with the author set to the full name
        
        thread.list_of_messages.add(message)
        thread.save()
        # Serialize the thread to return the updated thread data
        serializer = SerializeMessage(message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
class ThreadUpdateMessage(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, message_id, format=None):
        # Get the Thread object to associate the message with
        thread = get_object_or_404(Thread, pk=pk)

        # Get the Message object to update
        message = get_object_or_404(Message, pk=message_id)

        # Check if the authenticated user is the author of the message
        if message.author != request.user:
            return Response({"detail": "You do not have permission to update this message."}, status=status.HTTP_403_FORBIDDEN)

        # Update the message fields (e.g., body)
        message.body = request.data.get('body', message.body)
        message.save()  # Save the updated message

        # Serialize the updated thread with its messages
        serializer = SerializeMessage(message)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ThreadDeleteMessage(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk, message_id, format=None):
    # Get the Thread object
        thread = get_object_or_404(Thread, pk=pk)

        # Get the Message object to remove
        message = get_object_or_404(Message, pk=message_id)

        if message.author != request.user:
            return Response({"detail": "You do not have permission to delete this message."}, status=status.HTTP_403_FORBIDDEN)
        
        # Check if the message is part of the thread's list_of_messages
        if message not in thread.list_of_messages.all():
            return Response({"detail": "Message not found in this thread."}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the message from the thread
        thread.list_of_messages.remove(message)
        thread.save()
        message.delete()
        # Optionally, you can delete the message from the database
        # message.delete()  # Uncomment this line if you want to delete the message entirely

        # Serialize the updated thread data to return
        return Response({"detail": "Message deleted successfully."}, status=status.HTTP_200_OK)

        
