from rest_framework import serializers
from accounts.models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'about', 'company', 'is_vendor']


class CurrentUserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(source='userprofile_set', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'userprofile']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'about', 'company']