# Generated by Django 2.0.6 on 2018-07-10 15:53

import datetime
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=255, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='email or phone')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=255, verbose_name='phone')),
                ('fullname', models.CharField(max_length=255, null=True, verbose_name='phone')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('birthday', models.DateTimeField(default=datetime.date.today, verbose_name='birthday')),
                ('gender', models.IntegerField(choices=[('gender_male', 'male'), ('gender_female', 'female'), ('gender_other', 'other')], default=0)),
                ('signup_code', models.CharField(max_length=254, null=True, verbose_name='signup_code')),
            ],
            options={
                'verbose_name': 'UserAccount',
                'verbose_name_plural': 'UserAccounts',
                'ordering': ['username'],
                'abstract': False,
            },
        ),
    ]
