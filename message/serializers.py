from rest_framework import serializers
from profiles.serializers import SerializeProfile
from .models import Message

class SerializeMessage(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'author', 'description', 'timestamp']
        read_only_fields = ['id', 'timestamp']