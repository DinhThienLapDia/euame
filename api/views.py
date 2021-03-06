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

from .models import *
from .utils import send_email, send_sms

from stream_django.feed_manager import feed_manager

from api.enrich import Enrich
from api.enrich import did_i_feed_items
from api.enrich import do_i_friend_users

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

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
                        family_profile = UserProfile.objects.create(account=account,profile_type="family")
                        professional_profile = UserProfile.objects.create(account=account,profile_type="professional")
                        mask_profile = UserProfile.objects.create(account=account,profile_type="mask")
                        general_profile = UserProfile.objects.create(account=account,profile_type="general")
                        return Response({'status':"success",'userid':str(account.pk),"familyprofileid":family_profile.pk,"professionalprofileid":str(professional_profile.pk)
                            , "maskprofileid":str(mask_profile.pk), "generalprofileid":str(general_profile.pk)}, status=status.HTTP_200_OK)
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
                            family_profile = UserProfile.objects.filter(account=account,profile_type="family")[0]
                            professional_profile = UserProfile.objects.filter(account=account,profile_type="professional")[0]
                            mask_profile = UserProfile.objects.filter(account=account,profile_type="mask")[0]
                            general_profile = UserProfile.objects.filter(account=account,profile_type="general")[0]
                            return Response({'status':"success",'userid':str(account.pk),"familyprofileid":family_profile.pk,"professionalprofileid":str(professional_profile.pk)
                            , "maskprofileid":str(mask_profile.pk), "generalprofileid":str(general_profile.pk),"fullname":account.fullname}, 
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
                if "username" in request.data and "username_type" in request.data:
                    if not UserAccount.objects.filter(email_or_phone=request.data['username']):
                        return Response({'status':"user_not_exist"}, status=207)
                    signup_code = UserAccount.objects.get(email_or_phone=request.data['username']).signup_code
                    if request.data['username_type'] == "email":
                        mailjet = send_email()
                        data = {
                    'Messages': [
                    {
                        "From": {
                                "Email": "vneroica@gmail.com",
                                "Name": "euame"
                        },
                        "To": [
                                {
                                        "Email": request.data['username'],
                                        "Name": "Euame Customer"
                                }
                        ],
                        "Subject": "Your euame account recovery code",
                        "TextPart": "your recovery code is: " + signup_code,
                        "HTMLPart": "<h3>Dear new customer, your account recovery code is:" + signup_code +"</h3><br />please fill your code in the verfication screen of euame app"
                    }
                    ]
                    }
                        result = mailjet.send.create(data=data)
                        return Response({'status':"success"}, status=status.HTTP_200_OK)
                    if request.data['username_type'] == "phone":
                        content = "your verification code is " + signup_code 
                        send_sms(phone_number=request.data['username'],content=content)
                        return Response({'status':"success"}, status=status.HTTP_200_OK)
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
                if "code" in request.data and "userid" in request.data:
                    if request.data['code'] == UserAccount.objects.get(pk=request.data['userid']).signup_code:
                        return Response({'status':"success"}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status':"code_incorrect"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':"missing_params"}, status=400)
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
                    user = User.objects.get(username=request.data['username'])
                    user.set_password(request.data['newpassword'])
                    user.save()
                    return Response({'status':"success"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':"missing_params"}, status=400)
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
                if "code" in request.data and "username" in request.data:
                    if request.data['code'] == UserAccount.objects.get(email_or_phone=request.data['username']).signup_code:
                        return Response({'status':"success"}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status':"code_incorrect"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':"missing_params"}, status=400)
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
                return Response({'status':"missing_params"}, status=400)
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
                return Response({'status':"missing_params"}, status=400)
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
                return Response({'status':"missing_params"}, status=400)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "newpassword" in request.data and "userid" in request.data and "oldpassword" in request.data:
                    user = User.objects.get(pk=int(request.data['userid']))
                    if user.check_password(request.data['oldpassword']):
                        user.set_password(request.data['newpassword'])
                        user.save()
                        return Response({'status':"success"}, status=status.HTTP_200_OK)
                    else:
                        return Response({'status':"password_incorrect"}, status=400)
                else:
                    return Response({'status':"missing_params"}, status=400)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

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
                return Response({'status':"missing_params"}, status=400)
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
                return Response({'status':"missing_params"}, status=400)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ActivateProfile(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=400)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class SendProfileCode(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "fullname" in request.data and "profileid" in request.data and "profilecode" in request.data and "type" in request.dat and "to" in request.data:
                    
                    if request.data['type'] == "email":
                        mailjet = send_email()
                        data = {
                    'Messages': [
                    {
                        "From": {
                                "Email": "vneroica@gmail.com",
                                "Name": "euame"
                        },
                        "To": [
                                {
                                        "Email": request.data['to'],
                                        "Name": "Euame Customer"
                                }
                        ],
                        "Subject": request.data['fullname'] + " sent you a code add friend at euame",
                        "TextPart": "your friend code: " + request.data['profilecode'],
                        "HTMLPart": "<h3>Dear new customer, your friend code:" + request.data['profilecode'] +"</h3><br />please fill your code in the add friend screen of euame app"
                    }
                    ]
                    }
                        result = mailjet.send.create(data=data)
                        return Response({'status':"success"}, status=status.HTTP_200_OK)
                    if request.data['type'] == "phone":
                        content = "your verification code is " + request.data['profilecode']
                        send_sms(phone_number=request.data['to'],content=content)
                        return Response({'status':"success"}, status=status.HTTP_200_OK)
                else:
                    return Response({'status':"missing_params"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

class AddFriend(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=400)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class NewsFeed(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "userid" in request.data and "profileid" in request.data:
                    enricher = Enrich(User.objects.get(pk=request.data['userid']))
                    context = {}
                    feed = feed_manager.get_news_feeds(request.data['profileid'])['timeline_aggregated']
                    activities = feed.get(limit=25)['results']
                    context['activities'] = enricher.enrich_aggregated_activities(activities)
                    return Response({'status':"success",'feed':context}, status=status.HTTP_200_OK) 
                else:
                    return Response({'status':"missing_params"}, status=400)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

class NewPost(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "userid" in request.data and "postmessage" and "file" in request.data and "profileid" in request.data:
                    if request.FILES.get('filepath') == None:
                        userprofile = UserProfile.objects.get(pk=request.data['profileid'])
                        post = Post.objects.create(userprofile=userprofile,message=request.data['postmessage'],image=request.data['file'])
                    else:
                        userprofile = UserProfile.objects.get(pk=request.data['profileid'])
                        post = Post.objects.create(userprofile=userprofile,message=request.data['postmessage'],image=request.data['file'])
                    return Response({'status':"success"}, status=status.HTTP_200_OK) 
                else:
                    return Response({'status':"missing_params"}, status=400)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

class CommentPost(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=400)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class LikePost(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        if request.META.get('CONTENT_TYPE') == "application/json":
            if (request.data['username'] and request.data['password']):
                pass
            else:
                return Response({'status':"missing_params"}, status=400)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class Notifications(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "userid" in request.data and "profileid" in request.data:
                    enricher = Enrich(User.objects.get(pk=request.data['userid']))
                    context = {}
                    notifications = feed_manager.get_notification_feed(request.data['userid'])
                    activities = notifications.get(limit=25)['results']
                    print (activities)
                    activities =  serializers.serialize('json', activities)
                    #context['activities'] = enricher.enrich_aggregated_activities(activities)
                    return Response({'status':"success",'notifications':context}, status=status.HTTP_200_OK) 
                else:
                    return Response({'status':"missing_params"}, status=400)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)

class GetProfilesCode(APIView):
    #authentication_classes = 
    #permision_classes = 
    #rendered_classes = 
    def post(self, request, format = None):
        try:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if "userid" in request.data:
                    #enricher = Enrich(User.objects.get(pk=request.data['userid']))
                    #context = {}
                    account = UserAccount.objects.get(pk=request.data["userid"])
                    family_profile = UserProfile.objects.create(account=account,profile_type="family")
                    professional_profile = UserProfile.objects.create(account=account,profile_type="professional")
                    mask_profile = UserProfile.objects.create(account=account,profile_type="mask")
                    general_profile = UserProfile.objects.create(account=account,profile_type="general")
                    familyprofileicode = ""
                    professionalprofilecode = ""
                    maskprofilecode = ""
                    generalprofilecode = ""
                    if family_profile.pk < 10000000:
                        familyprofileicode = str(family_profile.pk + int(datetime.now().strftime("%H%M")))
                        professionalprofilecode = str(professional_profile.pk + int(datetime.now().strftime("%H%M")))
                        generalprofilecode = str(general_profile.pk + int(datetime.now().strftime("%H%M")))
                        maskprofilecode = str(mask_profile.pk + int(datetime.now().strftime("%H%M")))
                    else:
                        familyprofileicode = str(family_profile.pk)
                        professionalprofilecode = str(professional_profile.pk)
                        maskprofilecode = str(mask_profile.pk)
                        generalprofilecode = str(mask_profile.pk)
                    family_profile.profile_code = familyprofileicode
                    family_profile.save()
                    professional_profile.profile_code = professionalprofilecode
                    professional_profile.save()
                    general_profile.profile_code = generalprofilecode
                    general_profile.save()
                    mask_profile.profile_code = maskprofilecode
                    #context['activities'] = enricher.enrich_aggregated_activities(activities)
                    return Response({'status':"success","familyprofileicode":familyprofileicode,"professionalprofilecode":professionalprofilecode
                            , "maskprofilecode":maskprofilecode, "generalprofilecode":generalprofilecode}, status=status.HTTP_200_OK) 
                else:
                    return Response({'status':"missing_params"}, status=400)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':"server_exception",'details':str(e)}, status=501)


