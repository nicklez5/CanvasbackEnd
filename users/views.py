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
from .serializers import UserChangePasswordSerializer, UserSerializer, UserLoginSerializer, RegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken


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

class RegisterView(APIView):
    
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        reg_serializer = RegisterSerializer(data=request.data)
        data = {}
        if reg_serializer.is_valid():
            CustomUser = reg_serializer.save()
            data['response'] = "successfully registered a new user."
            data['email'] = CustomUser.email
            data['username'] = CustomUser.username
            (token,created) = Token.objects.get_or_create(user=CustomUser)
            data['token'] = token.key
        else:
            data = reg_serializer.errors
        return Response(data)
    
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
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
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