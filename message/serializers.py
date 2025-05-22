from rest_framework import serializers
from profiles.serializers import SerializeProfile
from .models import Message

class SerializeMessage(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'