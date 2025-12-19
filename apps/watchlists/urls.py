from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.watchlists.views import  WatchlistViewSet, WatchlistItemViewSet

# app_name = "users"

router = DefaultRouter()

router.register("watchlist", WatchlistViewSet, basename="watchlists")
router.register("watchlistitem", WatchlistItemViewSet, basename="watchlistitems")

urlpatterns = [
        # path("login/", UserLoginView.as_view(), name="login"),  
] + router.urls