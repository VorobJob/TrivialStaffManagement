from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from rest_framework.permissions import IsAuthenticated, AllowAny

from item.models import Subordination

from django.shortcuts import get_object_or_404

from item.serializators import UserCreateSerializer, UserListSerializer, SubordinateSerializer

import uuid
from rest_framework import generics
from .models import User

class UserEditView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer = UserListSerializer

    def patch(self, request, *args, **kwargs):
        user = request.user
        new_username = request.data.get('username')

        if new_username:
            user.username = new_username
            user.save()
        else:
            raise PermissionDenied(
            {"error": "Вы не предоставили username"})
        return Response(
            {"message": "Username успешно изменён."},
            status=status.HTTP_200_OK
        )
    
    
class UserDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer = UserListSerializer

    def delete(self, request, *args, **kwargs):
        boss = request.user
        sub_user = get_object_or_404(User, id=kwargs['id'])
        if not sub_user:
            raise PermissionDenied(
            {"error": "такого пользователя не существует"})

        if Subordination.objects.filter(
                boss=boss,
                subordinate=sub_user
        ):
            sub_user.delete()
            return Response({"message": "Подчинённый удален"})
        raise PermissionDenied(
            {"error": "Вы не являетесь боссом этого пользователя"})


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer: UserCreateSerializer):
        ref_code = self.request.data.get('ref_code')
        user = serializer.save(ref_code=uuid.uuid4())

        boss = User.objects.filter(ref_code=ref_code).first()

        Subordination.objects.create(subordinate=user, boss=boss)

        return user


class UserListView(generics.ListAPIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)


class SubordinatesView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Subordination.objects.filter(boss=request.user)
        serializer = SubordinateSerializer(queryset, many=True)
        return Response(serializer.data)
