from django.contrib.auth.models import update_last_login
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView 
from rest_framework import generics, status 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from .models import CustomUser 
from .serializers import ProfileSerializer,UserProfileCanvasSerializer,UserChangePasswordSerializer, UserSerializer, UserLoginSerializer, RegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import send_mail
class UserList(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self,request):
        queryset = CustomUser.objects.all() 
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class CustomAuthToken(ObtainAuthToken):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    def post(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        (token, created) = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'staff': user.is_staff
        })
class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Generate password reset token
        token = default_token_generator.make_token(user)

        # Create the password reset URL
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"http://localhost:8000/reset-password/{uid}/{token}/"

        # Send password reset email
        subject = "Password Reset Request"
        message = render_to_string("password_reset_email.html", {
            'user': user,
            'reset_url': reset_url,
        })
        send_mail(subject, message, "no-reply@example.com", [email])

        return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)
class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"detail": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get("password")
        if not new_password:
            return Response({"detail": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        CustomUser.set_password(new_password)
        CustomUser.save()

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
class RegisterView(APIView):
    
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        reg_serializer = RegisterSerializer(data=request.data)
        data = {}

        if reg_serializer.is_valid():
            # Check if the username or email already exists
            username = reg_serializer.validated_data['username']
            email = reg_serializer.validated_data['email']
            user_model = get_user_model()

            if user_model.objects.filter(username=username).exists():
                raise ValidationError({"username": "Username already exists."})
            if user_model.objects.filter(email=email).exists():
                raise ValidationError({"email": "Email is already registered."})

            # Save the new user
            user = reg_serializer.save()

            # Create a token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            # Send success response with the token and user data
            data['response'] = "Successfully registered a new user."
            data['email'] = user.email
            data['username'] = user.username
            data['token'] = token.key
            return Response(data, status=201)
        
        else:
            # If serializer is not valid, return errors
            data = reg_serializer.errors
            return Response(data, status=400)
    
class UserView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self,pk):
        try: 
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self,request,pk,format=None):
        custom_user = self.get_object(pk)
        serializer = UserSerializer(custom_user)
        return Response(serializer.data)
    
    def delete(self,request,pk,format=None):
        custom_user = self.get_object(pk)
        custom_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self,request,pk,format=None):
        custom_user = self.get_object(pk)
        serializer = UserSerializer(custom_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePassword(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def put(self,request,pk,format=None):
        custom_user = self.get_object(pk)
        serializer = UserChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not custom_user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            custom_user.set_password(serializer.data.get("new_password"))
            custom_user.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCanvasProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the logged-in user
        
        # Access the user profile and canvas
        profile = user.profile
        canvas = user.canvas
        
        # Serialize the profile and canvas data
        data = UserProfileCanvasSerializer({
            "profile": profile,
            "canvas": canvas
        }).data
        
        return Response(data)

# Create your views here.
# class CustomAuthToken(ObtainAuthToken):
#     serializer_class = UserLoginSerializer
#     permission_classes = [AllowAny]

#     def post(self,requesernst,*args, **kwargs):
#         serializer = self.serializer_class(data=request.data,context={'request':request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })