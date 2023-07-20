import uuid

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from item.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data, ref_code=uuid.uuid4())

    def validate(self, attrs):
        ref_code = self.context.get("ref_code")
        if not ref_code or not User.objects.filter(ref_code=ref_code):
            raise ValidationError({"error": "Неправильный реферальный код"})
        return attrs


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "ref_code")
