from apps.setup.models import AccountsTypeSetup, CurrencySetup, SMTPSettings, APIKey, WebhookSubscription
from apps.setup.serializers.api_key import APIKeySerializer
from apps.setup.serializers.smtp_settings import SMTPSettingsSerializer
from apps.setup.serializers.webhook_subscription import WebhookSubscriptionSerializer
from common_utils.response.mixins import ResponseHandlerMixin
from common_utils.views.mixins import AbstractViewSet
from common_utils.users.permissions import PermissionUtils, CustomPermissionClass
from common_utils.pagination.default_pagination import CustomDefaultPagination
from common_utils.cache.redis_cache import redis_client
from rest_framework.permissions import AllowAny
from apps.setup.serializers.account_type_setup import AccountsTypeSetupSerializer
from apps.setup.serializers.currency_setup import CurrencySetupSerializer


class AccountsTypeSetupViewSet(ResponseHandlerMixin, AbstractViewSet):
    queryset = AccountsTypeSetup.objects.filter()
    serializer_class = AccountsTypeSetupSerializer
    permission_classes = [CustomPermissionClass]
    pagination_class = CustomDefaultPagination

    # extra_permissions = [] # Example for adding extra permissions


class CurrencySetupViewSet(ResponseHandlerMixin, AbstractViewSet):
    queryset = CurrencySetup.objects.filter()
    serializer_class = CurrencySetupSerializer
    permission_classes = [CustomPermissionClass]
    pagination_class = CustomDefaultPagination

    extra_permissions = []  # Example for adding extra permissions


class SMTPSettingsViewSet(ResponseHandlerMixin, AbstractViewSet):
    queryset = SMTPSettings.objects.filter()
    serializer_class = SMTPSettingsSerializer
    permission_classes = [CustomPermissionClass]
    pagination_class = CustomDefaultPagination

    extra_permissions = []  # Example for adding extra permissions


class APIKeyViewSet(ResponseHandlerMixin, AbstractViewSet):
    queryset = APIKey.objects.filter().select_related('owner')
    serializer_class = APIKeySerializer  
    permission_classes = [CustomPermissionClass]
    pagination_class = CustomDefaultPagination

    extra_permissions = []  # Example for adding extra permissions


class WebhookSubscriptionViewSet(ResponseHandlerMixin, AbstractViewSet):
    queryset = WebhookSubscription.objects.filter().select_related('user')
    serializer_class = WebhookSubscriptionSerializer
    permission_classes = [CustomPermissionClass]
    pagination_class = CustomDefaultPagination

    extra_permissions = []  # Example for adding extra permissions