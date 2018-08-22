from django.db import models

""" EmailPhoneUser models."""
from django.contrib.auth.models import (
     PermissionsMixin, User
)
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

from mailjet_rest import Client

from twilio.rest import Client as Twilio

from stream_django.activity import Activity
from stream_django.feed_manager import feed_manager

from django.conf import settings




class EmailPhoneUserManager(models.Manager):

    """ Custom Manager for EmailPhoneUser.
    For Examples check Django code:
    """
    def normalize_email(self, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email

    def normalize_phone(self, phone, country_code=None):
        phone = phone.strip().lower()
        try:
            import phonenumbers
            phone_number = phonenumbers.parse(phone, country_code)
            phone = phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.E164)
        except ImportError:
            pass

        print(phone)

        return phone

    def _create_user(self, email_or_phone, password, fullname, gender,birthday,
                     is_staff, is_superuser, **extra_fields):
        """ Create EmailPhoneUser with the given email or phone and password.
        :param str email_or_phone: user email or phone
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return settings.AUTH_USER_MODEL user: user
        :raise ValueError: email or phone is not set
        :raise NumberParseException: phone does not have correct format
        """
        if not email_or_phone:
            raise ValueError('The given email_or_phone must be set')

        if "@" in email_or_phone:
            email_or_phone = self.normalize_email(email_or_phone)

            api_key = 'a0447053ba64e12d58c6f18ee42bcfc5'
            api_secret = '03d7d5b3791148902dcffd64edb62dbb'
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')

            signup_code = datetime.now().strftime('%M%m%H')

            data = {
            'Messages': [
                    {
                        "From": {
                                "Email": "vneroica@gmail.com",
                                "Name": "euame"
                        },
                        "To": [
                                {
                                        "Email": email_or_phone,
                                        "Name": fullname
                                }
                        ],
                        "Subject": "Your euame account verification code",
                        "TextPart": "your code is: " + signup_code,
                        "HTMLPart": "<h3>Dear new customer, your account verification code is:" + signup_code +"</h3><br />please fill your code in the verfication screen of euame app"
                    }
                    ]
            }

            result = mailjet.send.create(data=data)
            print(result.status_code)
            print(result.json())
                    

            username, email, phone = (email_or_phone, email_or_phone, "")

        else:
            phone = self.normalize_phone(email_or_phone)
            username, email = (email_or_phone, "")

            signup_code = datetime.now().strftime('%M%m%H')
            account_sid = 'AC4d3a68850fdbae49d26518b29c1e0404'
            auth_token = '65890d206e6755cf15afc2b3b5e6c0ee'
            client = Twilio(account_sid, auth_token)

            message = client.messages.create(
                              body='your euame verification code: ' + signup_code,
                              from_='+12243081374',
                              to=phone
                          )
            print(message.sid)

        now = timezone.now()
        is_active = extra_fields.pop("is_active", False)

        user = User.objects.create_user(username=username,password=password)
        user = self.model(
            user=user,
            email_or_phone=email_or_phone,
            email=email,
            phone=phone,
            fullname=fullname,
            gender=gender,
            birthday=birthday,
            signup_code=signup_code,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_user(self, email_or_phone, password=None, **extra_fields):
        return self._create_user(email_or_phone, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email_or_phone, password, **extra_fields):
        return self._create_user(email_or_phone, password, True, True,
                                 **extra_fields)


class UserAccount(models.Model):

    """ Abstract User with the same behaviour as Django's default User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)

    email_or_phone = models.CharField(
        _('email or phone'), max_length=255, unique=True, db_index=True, null= True,
        help_text=_('Required. 255 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[validators.RegexValidator(
            r'^[\w.@+-]+$', _(
                'Enter a valid username. '
                'This value may contain only letters, numbers '
                'and @/./+/-/_ characters.'
            ), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })

    email = models.EmailField(_('email'), max_length=254, blank=True)
    phone = models.CharField(_('phone'), max_length=255, blank=True)
    fullname = models.CharField(_('phone'), max_length=255, blank=False, null=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))

    is_superuser = models.BooleanField(
        _('superuser status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(
        _('active'), default=True, help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'))

    signed_in = models.BooleanField(
        _('signed_in'), default=False, help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'))

    is_verified = models.BooleanField(
        _('verified'), default=False, help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    """ Gender attribute of user. """

    gender_male = 0
    gender_female = 1
    gender_other = 2

    gender_choices = (('gender_male', 'male'), ('gender_female', 'female'), ('gender_other', 'other'))
    gender = models.CharField(choices=gender_choices)

    """ Birthday of user. """

    birthday = models.DateTimeField(_("birthday"), blank=True, null=True)

    last_login = models.DateTimeField(_("birthday"), blank=True, null=True)

    date_joined = models.DateTimeField(_("birthday"), blank=True, null=True)

    gender = models.IntegerField(choices=gender_choices,default=gender_male)

    signup_code = models.CharField(_('signup_code'), max_length= 254, blank=False,null=True)

    verify_code = models.CharField(_('verify_code'), max_length= 254, blank=False,null=True)

    objects = EmailPhoneUserManager()

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ["fullname"]

    def get_full_name(self):
        """ Return the full name for the user."""
        return self.fullname

    def get_short_name(self):
        """ Return the short name for the user."""
        return self.fullname

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class BaseModel(models.Model):
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class UserProfile(models.Model):
    profile_family = "family"
    profile_professional = "professional"
    profile_mask = "mask"
    profile_general = "general"
    profile_choices = (('profile_family','family'),('profile_professional','professional'),('profile_mask','mask'),('profile_general','general'))

    profile_code = models.CharField(_('profile_code'), max_length= 254, blank=False,null=True)

    profile_type = models.CharField(choices=profile_choices,max_length=255)
    account = models.ForeignKey(
        UserAccount, related_name='account',on_delete=models.CASCADE)

    is_active = models.BooleanField(
        _('active'), default=False, help_text=_(
            'Designates whether this profile should be treated as active. '
            'Unselect this instead of deleting accounts.'))

    def __str__(self):
        return self.profile_type

    class Meta:
        ordering = ["profile_type"]




class Post(BaseModel):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='postimages/%Y/%m/%d')
    source_url = models.TextField()
    message = models.TextField(blank=True, null=True)
    pin_count = models.IntegerField(default=0)

class Feed(Activity, BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)
    item = models.ForeignKey(Post, on_delete=models.CASCADE)
    influencer = models.ForeignKey(
        UserProfile, related_name='influenced_pins',on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)

    @classmethod
    def activity_related_models(cls):
        return ['user', 'post']

    @property
    def activity_object_attr(self):
        return self

    @property
    def extra_activity_data(self):
        return dict(item_id=self.item_id)

    @property
    def activity_notify(self):
        target_feed = feed_manager.get_notification_feed(self.friend_id)
        return [target_feed]


class Friend(Activity, BaseModel):
    '''
    A simple table mapping who a user is following.
    For example, if user is Kyle and Kyle is following Alex,
    the target would be Alex.
    '''
    user = models.ForeignKey(
        UserProfile, related_name='following_set',on_delete=models.CASCADE, default=None)
    friend = models.ForeignKey(
        UserProfile, related_name='follower_set',on_delete=models.CASCADE, default=None)

    @classmethod
    def activity_related_models(cls):
        return ['user', 'friend']

    @property
    def activity_object_attr(self):
        return self

    @property
    def activity_notify(self):
        target_feed = feed_manager.get_notification_feed(self.friend_id)
        return [target_feed]



def soft_delete(sender, instance, **kwargs):
    if instance.deleted_at is not None:
        feed_manager.activity_delete(sender, instance, **kwargs)
