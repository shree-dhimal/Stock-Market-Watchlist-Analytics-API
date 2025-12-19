from common_utils.response.mixins import ResponseHandlerMixin
from common_utils.views.mixins import AbstractViewSet
from common_utils.users.permissions import PermissionUtils, CustomPermissionClass
from common_utils.pagination.default_pagination import CustomDefaultPagination

from apps.notifications.models import PriceAlert
from apps.notifications.serializers.price_alert import PriceAlertSerializer


class PriceAlertViewSet(AbstractViewSet,ResponseHandlerMixin):
    queryset = PriceAlert.objects.filter(is_active=True).select_related('user', 'stock')
    serializer_class = PriceAlertSerializer
    permission_classes = [CustomPermissionClass]
    pagination_class = CustomDefaultPagination
    # extra_permissions = [] # Define any extra permissions if needed like {actions}_{model}