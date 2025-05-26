from rest_framework import serializers
from course.serializers import SerializeCourse
from users.serializers import UserSerializer
from .models import Canvas
class SerializeCanvas(serializers.ModelSerializer):
    list_courses = SerializeCourse(many=True)
    user = UserSerializer(read_only=True,many=False)
    class Meta:
        model = Canvas 
        fields = '__all__'