from django.shortcuts import render
from .models import Message
from users.models import CustomUser
from profiles.models import Profile 
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import serializers, status
from .serializers import SerializeMessage
class MessageList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, reuqest, format=None):
        messages = Message.objects.all()
        serializer = SerializeMessage(messages,many=True)
        return Response(serializer.data)

class MessagePost(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = SerializeMessage(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404
    
    def get(self, request, pk , format=None):
        message = self.get_object(pk)
        serializer = SerializeMessage(message)
        return Response(serializer.data)

class MessageUpdate(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self,pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        message = self.get_object(pk)
        serializer = SerializeMessage(message,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageDelete(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self,pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404
    
    def delete(self, request, pk ,format=None):
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
# Create your views here.