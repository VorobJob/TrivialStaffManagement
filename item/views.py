from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from item.models import User
from item.models import Subordination

from django.shortcuts import get_object_or_404

from item.serializators import UserCreateSerializer, UserListSerializer


class UserDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    # Delete
    def delete(self, request, *args, **kwargs):
        boss = request.user
        sub_user = get_object_or_404(User, id=kwargs['id'])
        if Subordination.objects.filter(
                boss=boss,
                subordinate=sub_user
        ):
            sub_user.delete()
            return Response({"info": "Подчинённый удален"})
        raise PermissionDenied({"error": "Вы не являетесь боссом этого пользователя"})
    
    # Read
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs['id'])
        return Response(UserListSerializer(user).data)

    #Update
    def patch(self, request, *args, **kwargs):
        boss = request.user
        sub_user = get_object_or_404(User, id=kwargs['id'])
        if Subordination.objects.filter(
                boss=boss,
                subordinate=sub_user
        ):
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if username:
                sub_user.username = username
            if password:
                sub_user.set_password(password)
            
            # Save the updated User instance
            sub_user.save()
            
            return Response({"message": "Учетная запись подчинённого изменена"}, status=status.HTTP_200_OK)
        return Response({"message": "You do not have permission to update this user"}, status=status.HTTP_400_BAD_REQUEST)


class SubordinatesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        subs = [sub.subordinate for sub in Subordination.objects.filter(boss=request.user)]
        return Response(UserListSerializer(subs, many=True).data)


class UserListCreateView(APIView):
    serializer_class = UserCreateSerializer

    def get(self, request, *args, **kwargs):
        return Response(UserListSerializer(User.objects.all()[0:20], many=True).data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={
            "ref_code": request.data.get("ref_code")
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_boss = User.objects.get(ref_code=request.data.get("ref_code"))
        Subordination.objects.create(
            subordinate=serializer.instance,
            boss=user_boss
        )
        return Response({"info": f"Пользователь {serializer.instance.username} создан"}, status=status.HTTP_201_CREATED)

# class UserGetView(APIView):
#     permission_classes = (IsAuthenticated, )
#
#     def get(self, request):
#         return Response(request.user)
