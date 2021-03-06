"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, re_path
    2. Add a URL to urlpatterns:  re_path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, include
import api.views as api

urlpatterns = [
	re_path(r'^', include('api.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/v1/useraccount/signup/', api.AccountSignup.as_view()),
    re_path(r'^api/v1/useraccount/signin/', api.AccountSignin.as_view()),
    re_path(r'^api/v1/useraccount/signout/', api.AccountSignout.as_view()),
    re_path(r'^api/v1/useraccount/lostpassword/', api.LostPassword.as_view()),
    re_path(r'^api/v1/useraccount/verifyaccount/', api.VerifyAccount.as_view()),
    re_path(r'^api/v1/useraccount/editaccount/', api.EditAccount.as_view()),
    re_path(r'^api/v1/useraccount/accountsetting/', api.AccountSetting.as_view()),
    re_path(r'^api/v1/useraccount/getaccountdetails/', api.GetAccountDetails.as_view()),
    re_path(r'^api/v1/useraccount/lostpasswordnewpassword/', api.LostPasswordNewPassword.as_view()),
    re_path(r'^api/v1/useraccount/lostpasswordverifycode/', api.LostPasswordVerifyCode.as_view()),
    re_path(r'^api/v1/useraccount/changepassword/', api.ChangePassword.as_view()),
    re_path(r'^api/v1/useraccount/resendcode/', api.ResendCode.as_view()),
    re_path(r'^api/v1/useraccount/activateprofile/', api.ActivateProfile.as_view()),
    re_path(r'^api/v1/useraccount/sendprofilecode/', api.SendProfileCode.as_view()),
    re_path(r'^api/v1/useraccount/addfriend/', api.AddFriend.as_view()),  
    re_path(r'^api/v1/useraccount/newsfeed/', api.NewsFeed.as_view()),
    re_path(r'^api/v1/useraccount/notifications/', api.Notifications.as_view()), 
    re_path(r'^api/v1/useraccount/likepost/', api.LikePost.as_view()),
    re_path(r'^api/v1/useraccount/newpost/', api.NewPost.as_view()),
    re_path(r'^api/v1/useraccount/commentpost/', api.CommentPost.as_view()), 
    re_path(r'^api/v1/useraccount/getprofilescode/', api.GetProfilesCode.as_view()),
]
