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
class MessageList(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = SerializeMessage
    permission_classes = [IsAuthenticated]


class MessageCreateView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = SerializeMessage
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        # Fetch the updated thread, without querying again if already loaded
        thread = message.thread

        # Optionally handle thread not found, although it should exist due to ForeignKey constraint
        if not thread:
            return Response({"detail": "Thread not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the updated thread data
        thread_data = SerializeThread(thread).data
        return Response(thread_data, status=status.HTTP_201_CREATED)

class MessageDetailView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = SerializeMessage
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class MessageUpdateView(UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = SerializeMessage
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class MessageDeleteView(DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = SerializeMessage
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


    
# Create your views here.