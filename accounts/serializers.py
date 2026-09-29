import re
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        write_only=True,
        required=True
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ["name","username","email","phone_no","password"]

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exist"
            )
        return value

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exist"
            )
        return value 


    def validate_phone(self, value):
        if value:
            value = value.strip()
            if not value.isdigit():
                raise serializers.ValidationError(
                    "Phone number must contain only digits."
                )
            if len(value) != 10:
                raise serializers.ValidationError(
                    "Phone number must contain 10 digits."
                )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id","username","email","name","phone_no","role","date_joined"]
        read_only_fields = ["id","role","date_joined"]