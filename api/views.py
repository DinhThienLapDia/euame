from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
#from rest_framework.authentication import (TokenAuthentication,
#                                           SessionAuthentication)
#from rest_framework.permissions import IsAuthenticated
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser

from datetime import datetime

from .models import UserAccount

class AccountSignup(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        #signup new account
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if ("username" in request.data and "password" in request.data and "gender" in request.data and "birthday" in request.data and "fullname" in request.data):
                    if User.objects.filter(username=request.data['username']).exists():
                        return Response({'status':"user_existed"}, status=588)
                    else:
                        birthday = datetime.strptime(request.data['birthday'],"%d%m%Y").date()
                        UserAccount.objects._create_user(request.data['username'], request.data['password'], request.data['fullname'], request.data['gender'],
                        birthday, False, False)
                        return Response({'status':"success"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':"missing_params"}, status=589)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception"}, status=501)

class AccountSignin(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format=None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if ("username" in request.data and "password" in request.data):
                user = User.objects.get(username=request.data['username'])
                if user.check_password(request.data['password']):
                    return Response({'status':"success",'userid':user.pk,'fullname':UserAccount.objects.get(pk=user.pk).fullname},status=status.HTTP_200_OK)
                else:
                    return Response({'status':"incorrect"}, status=590)
            else:
                return Response({'status':"missing_params"}, status=589)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class AccountSignout(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=701)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LostPassword(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=701)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class VerifyAccount(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=701)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LostPasswordNewPassword(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=701)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LostPasswordVerifyCode(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=701)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GetAccountDetails(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=701)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class EditAccount(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=701)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class AccountSetting(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=701)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


