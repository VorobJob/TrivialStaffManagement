from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from item.views import UserListCreateView, SubordinatesView, UserDeleteView

urlpatterns = [
    path("subordinates/", SubordinatesView.as_view()),

    path("users/", UserListCreateView.as_view()),
    path("users/<int:id>/", UserDeleteView.as_view()), 
    # path("users/me/", UserGetView.as_view()),


    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
