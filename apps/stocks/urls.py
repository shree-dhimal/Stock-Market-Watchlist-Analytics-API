from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.stocks.views import  StockViewSet

# app_name = "users"

router = DefaultRouter()

router.register("stock", StockViewSet, basename="stocks")

urlpatterns = [
        # path("login/", UserLoginView.as_view(), name="login"),  
] + router.urls