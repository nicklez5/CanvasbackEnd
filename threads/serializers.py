from rest_framework import serializers
from message.serializers import SerializeMessage
from profiles.serializers import SerializeProfile
from .models import Thread
class SerializeThread(serializers.ModelSerializer):
    list_of_messages = SerializeMessage(many=True, read_only=True) 
    class Meta:
        model = Thread
        fields =  ['id','title','list_of_messages', 'created_at']