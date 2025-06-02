from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, generics 
from .models import CustomUser, Profile, Canvas


class UserSerializer(serializers.ModelSerializer):
    pk       = serializers.IntegerField(read_only=True, source="id")
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model  = CustomUser
        fields = ["pk", "email", "username", "is_staff"]

    def validate_email(self, value):
        # Ensure no other user already has this email
        user = self.context["request"].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_username(self, value):
        # Ensure no other user already has this username
        user = self.context["request"].user
        if CustomUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("Username is already in use.")
        return value

    def update(self, instance, validated_data):
        # Only allow updating email & username
        instance.email    = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for handling password change:
    - current_password
    - new_password
    - confirm_new_password
    """
    current_password     = serializers.CharField(write_only=True)
    new_password         = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, data):
        new_pw  = data.get("new_password")
        confirm = data.get("confirm_new_password")
        if new_pw != confirm:
            raise serializers.ValidationError({"confirm_new_password": "Passwords do not match."})
        # Let Django’s password validators run (e.g. min length, complexity)
        validate_password(new_pw, user=self.context["request"].user)
        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self,value):
        validate_password(value)
        return value

    
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    role = serializers.ChoiceField(
        choices=[("Student", "Student"), ("Staff", "Staff")],
        write_only=True,
        default="Student",
    )

    class Meta:
        model = get_user_model()
        fields = ['username','email','password', 'password2',"role"]
        extra_kwargs = {'password': {'write_only': True}}
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs
    def create(self, validated_data):
        """Create a user and return it."""
        role = validated_data.pop("role", "Student")
        validated_data.pop('password2', None)
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
         # Hash the password
        if role == "Staff":
            user.is_staff = True
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


        