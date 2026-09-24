from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Address

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile, _ = UserProfile.objects.get_or_create(user=instance)
        profile.phone = profile_data.get('phone', profile.phone)
        profile.save()

        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'label', 'full_name', 'phone', 'address', 'city', 'state', 'pincode', 'is_default']