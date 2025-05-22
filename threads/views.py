from django.shortcuts import render

from users.models import CustomUser
from profiles.models import Profile 
from .models import Thread
from django.http import Http404
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

class ThreadList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SerializeThread

    def get(self, request, format=None):
        thread = Thread.objects.all()
        serializer = self.serializer_class(thread,many=True)
        return Response(serializer.data)

class ThreadView(APIView):
    serializer_class = SerializeThread
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def get(self, request, pk, format=None):
        thread = self.get_object(pk)
        serializer = SerializeThread(thread)
        return Response(serializer.data)



class ThreadPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request,format=None):
        
        serializer = SerializeThread(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ThreadDelete(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self,pk):
        try:
            return Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def delete(self, request, pk , format=None):
        thread = self.get_object(pk)
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ThreadMessage(APIView):
    serializer_class = SerializeThread
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def post(self,request,pk,format=None):
        data = request.data
        thread = self.get_object(pk)
        msg_id = data['id']
        msg_author = data["author"]
        msg_description = data["description"]
        msg_timestamp = data["timestamp"]
        try:
            msg = Message.objects.get(pk=msg_id)
        except Message.DoesNotExist:
            msg = Message.objects.create(author = msg_author, description=msg_description,timestamp = msg_timestamp)
        finally:
            thread.list_messages.add(msg)
            thread.last_author = msg.author
            thread.last_description = msg.description
            thread.last_timestamp = msg.timestamp
            thread.save()
            serializer = SerializeThread(thread)
            return Response(serializer.data)

    
    def delete(self,request,pk,format=None):
        data = request.data
        thread = self.get_object(pk)
        msg_id = data["id"]
        try:
            msg = Message.objects.get(pk=msg_id)
            thread.list_messages.remove(msg)
            if thread.list_messages.exists():
                last_msg = thread.list_messages.last()
                thread.last_author = last_msg.author
                thread.last_description = last_msg.description
                thread.last_timestamp = last_msg.timestamp
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        finally:
            thread.save()
            serializer = SerializeThread(thread)
            return Response(serializer.data)

        
