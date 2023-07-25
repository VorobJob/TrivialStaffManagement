from .models import Subordination
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework.exceptions import ValidationError


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'ref_code')

    def validate_password(self, password):
        validate_password(password)
        return password

    def create(self, validated_data: dict):
        password = validated_data.pop('password')
        user: User = super().create(validated_data)

        try:
            user.set_password(password)
            user.save()
            return user
        except serializers.ValidationError as exc:
            user.delete()
            raise exc

    def validate_ref_code(self, ref_code):
        user = User.objects.filter(ref_code=ref_code)
        if not user:
            return ValidationError('Nety refcoda')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "ref_code")


class SubordinateSerializer(serializers.ModelSerializer):
    subordinate = UserListSerializer()
    boss = UserListSerializer()

    class Meta:
        model = Subordination
        fields = ("id", "subordinate", "boss")
