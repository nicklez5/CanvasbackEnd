from rest_framework import serializers
from message.serializers import SerializeMessage
from profiles.serializers import SerializeProfile
from .models import Thread
class SerializeThread(serializers.ModelSerializer):
    list_messages = SerializeMessage(read_only=True,many=True)
    class Meta:
        model = Thread
        fields = '__all__'
        depth = 1