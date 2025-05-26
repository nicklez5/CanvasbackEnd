from rest_framework import serializers
from message.serializers import SerializeMessage
from profiles.serializers import SerializeProfile
from .models import Thread
class SerializeThread(serializers.ModelSerializer):
    messages = SerializeMessage(many=True, read_only=True) 
    class Meta:
        model = Thread
        fields =  ['id','last_author', 'last_description', 'last_timestamp', 'messages']