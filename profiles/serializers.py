from rest_framework import serializers
from django.db import models 
from .models import Profile 
class SerializeProfile(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True,source='user.email')
    class Meta:
        model = Profile 
        fields = ['pk','email','first_name','last_name','date_of_birth']

    def update(self,instance,validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth',instance.date_of_birth)
        instance.save()
        return instance 

    