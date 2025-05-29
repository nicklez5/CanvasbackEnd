from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, generics 
from .models import CustomUser, Profile, Canvas


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','pk','is_staff']


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self,value):
        validate_password(value)
        return value

    
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = get_user_model()
        fields = ['username','email','password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}
    def validate(self, attrs):
        """Ensure both passwords match."""
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        
        return attrs
    def create(self, validated_data):
        """Create a user and return it."""
        password = validated_data.pop('password')  # Pop password field
        user = get_user_model().objects.create_user(**validated_data)  # Create user with hashed password
        user.set_password(password)  # Hash the password
        user.save()  # Save the user to the database
        return user
    def save(self):
        user = CustomUser(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user 
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128,write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                _("Must include both email and password."), code="authorization"
            )

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                _("Unable to log in with provided credentials."), code="authorization"
            )

        if not user.is_active:
            raise serializers.ValidationError(
                _("User account is disabled."), code="authorization"
            )

        data["user"] = user
        return data
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth']

class CanvasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canvas
        fields = ['list_courses']  # You can include other fields as needed

class UserProfileCanvasSerializer(serializers.Serializer):
    profile = ProfileSerializer()
    canvas = CanvasSerializer()


        