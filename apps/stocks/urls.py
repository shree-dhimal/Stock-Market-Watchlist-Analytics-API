from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.stocks.views import  StockViewSet

# app_name = "users"

router = DefaultRouter()

router.register("stock", StockViewSet, basename="users")

urlpatterns = [
        # path("login/", UserLoginView.as_view(), name="login"),  
] + router.urls