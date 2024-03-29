from django.test import TestCase

# Create your tests here.

#model
import os
from uuid import uuid4
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# below imports are for global services localizations
# from django.utils import timezone 
# from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, userid, email, password, **extra_fields):
        if not userid:
            raise ValueError("Users must have an userid")
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(userid=userid, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, userid, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        return self._create_user(userid, email, password, **extra_fields)

    # def create_superuser(self, userid, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')
    #     return self._create_user(userid, email, password, **extra_fields)


def upload_to_func_common(instance, filename):
    prefix = timezone.now().strftime("%Y/%m/%d")
    file_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower() # 확장자 추출
    return "/".join(
        [str(instance.filesavefield), prefix, file_name+extension]
    )

class User(AbstractBaseUser):
    userid = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=16)
    num = models.CharField(max_length=12, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'userid'
    # REQUIRED_FIELDS = ['userid']
    
    class Meta:
        db_table = 'kingbus_user'

    def __str__(self):
        return self.userid


class DriverAcc(AbstractBaseUser):
    userid = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=16)
    num = models.CharField(max_length=12, unique=True)
    driver_com_name = models.CharField(max_length=32)
    driver_car_driverlisence = models.ImageField(upload_to=upload_to_func_common)
    # Profile section below
    driver_car_option = models.CharField(max_length=128, null=True, blank=True)
    driver_car_num = models.CharField(max_length=10, null=True, blank=True)
    driver_car_kind = models.CharField(max_length=32, null=True, blank=True)
    driver_car_year = models.CharField(max_length=4, null=True, blank=True)
    driver_car_photo = models.ImageField(upload_to='driver_carphoto/', null=True, blank=True) # try to use 1:1 rel for upload_to func usage. TODO
    driver_profile_tradeunion_certificate = models.FileField(upload_to='driver_tradeunion_certificate/', null=True, blank=True) # try to use 1:1 rel for upload_to func usage. TODO
    driver_profile_introduction = models.CharField(max_length=200, null=True, blank=True)
    driver_profile_introduction_video = models.TextField(null=True, blank=True)
    #models.FileField(upload_to="driver_introduction_video"+str(upload_to_func_common), null=True, blank=True) # TODO Youtube or File upload
    driver_profile_location = models.CharField(max_length=128, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kingbus_driveracc'

    objects = UserManager()

    USERNAME_FIELD = 'userid'
    # REQUIRED_FIELDS = ['userid']
    filesavefield = 'driveracc'


class CompanyAcc(AbstractBaseUser):
    userid = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=255, unique=True)# manager's email
    name = models.CharField(max_length=16)# manager's name
    num = models.CharField(max_length=12, unique=True)
    company_com_name = models.CharField(max_length=32)
    company_business_registration = models.ImageField(upload_to=upload_to_func_common)
    # Profile section below
    company_profile_transportationbusiness_registration = models.ImageField(upload_to='company_transportationbusiness_registration/', null=True, blank=True) # try to use 1:1 rel for upload_to func usage. TODO
    company_profile_tradeunion_certificate = models.FileField(upload_to='company_profile_tradeunion_certificate/', null=True, blank=True) # try to use 1:1 rel for upload_to func usage. TODO
    company_profile_introduction = models.CharField(max_length=200, null=True, blank=True)
    company_profile_introduction_video = models.TextField(null=True, blank=True)
    #models.FileField(upload_to="company_introduction_video"+str(upload_to_func_common), null=True, blank=True)
    company_profile_location = models.CharField(max_length=128, null=True, blank=True)
    company_profile_companylocation = models.CharField(max_length=128, null=True, blank=True)
    company_profile_vehiclecount = models.CharField(max_length=8, null=True, blank=True)
    company_code = models.CharField(max_length=12, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kingbus_companyacc'

    objects = UserManager()

    USERNAME_FIELD = 'userid'
    # REQUIRED_FIELDS = ['userid']
    filesavefield = 'companyacc'


#serializers
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, DriverAcc, CompanyAcc
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.hashers import check_password


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError("Invalid login credentials")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid password")
    
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        # update_last_login(None, user)
        validation = {
            'access': access_token,
            'refresh': refresh_token,
            'username': user.username,
        }
        return validation

class DriverLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    def validate(self, data):
        try:
            driver = DriverAcc.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError("Invalid login credentials")
        if not driver.check_password(data['password']):
            raise serializers.ValidationError("Invalid password")
    
        refresh = RefreshToken.for_user(driver)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        # update_last_login(None, user)
        validation = {
            'access': access_token,
            'refresh': refresh_token,
            'username': driver.username,
        }
        return validation

class CompanyLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    def validate(self, data):
        try:
            company = CompanyAcc.objects.get(username=data['username'])
        except:
            raise serializers.ValidationError("Invalid login credentials")
        if not company.check_password(data['password']):
            raise serializers.ValidationError("Invalid password")
    
        refresh = RefreshToken.for_user(company)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        # update_last_login(None, user)
        validation = {
            'access': access_token,
            'refresh': refresh_token,
            'username': company.username,
        }
        return validation


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'name' , 'num')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_date):
        user = User.objects.create_user(**validated_date)
        #     username=validated_date['username'],
        #     email=validated_date['email'],
        #     password=validated_date['password'],
        #     name=validated_date['name'],
        # )
        return user


class DriverRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverAcc
        fields = ('username', 'password', 'email', 'name' , 'num', 'driver_com_name', 'driver_car_driverlisence')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_date):
        driver = DriverAcc.objects.create_user(**validated_date)
        return driver


class CompanyRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAcc
        fields = ('username', 'password', 'email', 'name' , 'num', 'company_com_name', 'company_business_registration')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_date):
        company = CompanyAcc.objects.create_user(**validated_date)
        return company

