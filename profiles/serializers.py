from rest_framework import serializers
from django.db import models 
from .models import Profile 
class SerializeProfile(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True,source='user.email')
    class Meta:
        model = Profile 
        fields = ['id','email','first_name','last_name','date_of_birth']
    
    