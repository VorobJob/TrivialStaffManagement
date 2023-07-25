from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from item.views import UserCreateView, UserListView, SubordinatesView, UserDeleteView, UserEditView

urlpatterns = [
    path("subordinates/", SubordinatesView.as_view()),

    path("list_users/", UserListView.as_view()),
    path("create_user/", UserCreateView.as_view()),
    path("delete_user/<int:id>/", UserDeleteView.as_view()),
    path("edit_user/<int:id>/", UserEditView.as_view()),

    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]

# johnJohns
# Vodka
