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
    #authentication_classes = TokenAuthentication
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
                        birthday = ""
                        try:
                            birthday = datetime.strptime(request.data['birthday'],"%d%m%Y").date()
                        except Exception as e:
                            return Response({'status':"bad_request","details":str(e)}, status=400)
                        account = UserAccount.objects._create_user(request.data['username'], request.data['password'], request.data['fullname'], request.data['gender'],
                        birthday, False, False)
                        return Response({'status':"success",'userid':account.pk},, status=status.HTTP_200_OK)
                else:
                    return Response({'status':"missing_params"}, status=589)
            else:
                return Response({'status':"missing_params"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception"}, status=501)

class AccountSignin(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format=None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "username" in request.data and "password" in request.data:
                    if User.objects.filter(username=request.data['username']).exists():
                        if User.objects.get(username=request.data['username']).check_password(request.data['password']):
                            user = User.objects.get(username=request.data['username'])
                            account = UserAccount.objects.get(email_or_phone=request.data['username'])
                            account.signed_in = True
                            account.save()
                            return Response({'status':"success","userid":user.pk,"fullname":account.fullname}, 
                                status=status.HTTP_200_OK)
                        else:
                            return Response({'status':"password_incorrect"}, status=590)
                    else:
                        return Response({'status':"username_incorrect"}, status=590)
                else:
                    return Response({'status':"missing_params"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception"}, status=501)

class AccountSignout(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "userid" in request.data:
                    user = User.objects.get(pk=int(request.data['userid']))
                    account = UserAccount.objects.get(email_or_phone=user.username)
                    account.signed_in = False
                    account.save()
                    return Response({'status':"success"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':"missing_params"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

class LostPassword(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "username" in request.data:
                    if User.objects.filter(username=request.data['username']).exists():
                        verify_code = "1234"
                        return Response({'status':"success",'verify_code':verify_code}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status':"username_incorrect"}, status=590)
                else:
                    return Response({'status':"missing_params"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

class VerifyAccount(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "code" in request.data:
                    if request.data['code'] == "1234":
                        return Response({'status':"success"}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status':"code_incorrect"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':"missing_params"}, status=701)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

class LostPasswordNewPassword(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "newpassword" in request.data and "username" in request.data:
                    User.objects.get(username=request.data['username']).set_password(request.data['newpassword']).save()
                    return Response({'status':"code_incorrect"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':"missing_params"}, status=701)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

class LostPasswordVerifyCode(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "code" in request.data:
                    if request.data['code'] == "1234":
                        return Response({'status':"success"}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status':"code_incorrect"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':"missing_params"}, status=701)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

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

class ChangePassword(APIView):
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

class ResendCode(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "username" in request.data:
                    if User.objects.filter(username=request.data['username']).exists():
                        verify_code = "1234"
                        return Response({'status':"success",'verify_code':verify_code}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status':"username_incorrect"}, status=590)
                else:
                    return Response({'status':"missing_params"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

class DeactivateAccount(APIView):
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

class DeleteAccount(APIView):
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



