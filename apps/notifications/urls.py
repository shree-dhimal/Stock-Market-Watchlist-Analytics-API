from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.notifications.views import PriceAlertViewSet

# app_name = "users"

router = DefaultRouter()

router.register("price-alert", PriceAlertViewSet, basename="price-alerts")

urlpatterns = [
        # path("login/", UserLoginView.as_view(), name="login"),  # Token generation
] + router.urls