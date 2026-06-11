from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import random

import random

class RegisterSerializer(serializers.ModelSerializer):    
    class Meta:
        model = MyUser
        fields = ['name', 'email', 'password']
    
    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        user.otp = str(random.randint(100000, 999999))
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = MyUser.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError('User not Found!!!')
        
        user = authenticate(email=email, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials!!')
        
        attrs['user'] = user
        return attrs
    
    
class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        user = MyUser.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError('User not Found!!!')
        
        if user.otp != otp:
            raise serializers.ValidationError('Invalid OTP!!')

        user.is_active = True
        user.otp = ""
        user.save()

        attrs['user'] = user
        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        refresh_token = self.validated_data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()