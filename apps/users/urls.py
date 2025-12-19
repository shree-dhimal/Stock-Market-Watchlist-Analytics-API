from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.views import  AssignGroupUserView, CreateGroupsPermissionsView, GetAllGroupsView, GetAllPermissionsView, GetUserSelfView, UserLoginView, UserLogoutView, UserViewSet

# app_name = "users"

router = DefaultRouter()

router.register("user", UserViewSet, basename="users")

urlpatterns = [
        path("login/", UserLoginView.as_view(), name="login"),  # Token generation
        path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path("logout/", UserLogoutView.as_view(), name="user-logout"),
        path("all-permissions/", GetAllPermissionsView.as_view(), name="all-permissions"),
        path("all-groups/", GetAllGroupsView.as_view(), name="all-groups"),
        path("all-groups/<int:id>/", GetAllGroupsView.as_view(), name="all-groups-detail"),
        path("create-groups-permissions/", CreateGroupsPermissionsView.as_view(), name="create-groups-permissions"),
        path("assign-groups-to-user/", AssignGroupUserView.as_view(), name="assign-groups-to-user"),
        path("user/self/", GetUserSelfView.as_view(), name="user-self"),
] + router.urls