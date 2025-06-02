from rest_framework import serializers
from assignments.serializers import AssignmentSerializer
from lectures.serializers import SerializeLecture
from profiles.serializers import SerializeProfile
from tests.serializers import TestSerializer
from threads.serializers import SerializeThread
from .models import Course 
class SerializeCourse(serializers.ModelSerializer):
    assignments = AssignmentSerializer(read_only=True, many=True)
    lectures = SerializeLecture(read_only=True,many=True)
    profiles = SerializeProfile(read_only=True,many=True)
    tests = TestSerializer(read_only=True,many=True)
    threads = SerializeThread(read_only=True,many=True)
    class Meta:
        model = Course 
        fields = ['id','name','assignments','lectures','profiles','tests','threads']
        depth = 1