from rest_framework import serializers
from .models import Tests

class SerializeTest(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = '__all__'
