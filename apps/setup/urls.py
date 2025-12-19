from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.setup.views import  AccountsTypeSetupViewSet, CurrencySetupViewSet, SMTPSettingsViewSet, APIKeyViewSet, WebhookSubscriptionViewSet

# app_name = "users"

router = DefaultRouter()

router.register("account-type", AccountsTypeSetupViewSet, basename="account-types")
router.register("currency", CurrencySetupViewSet, basename="account-types")
router.register("smtp-settings", SMTPSettingsViewSet, basename="smtp-settings")
router.register("api-key", APIKeyViewSet, basename="api-keys")
router.register("webhook-subscription", WebhookSubscriptionViewSet, basename="webhook-subscriptions")

urlpatterns = [
        # path("login/", UserLoginView.as_view(), name="login"),  
] + router.urls

