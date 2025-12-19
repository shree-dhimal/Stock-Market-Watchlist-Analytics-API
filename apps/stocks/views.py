from apps.stocks.serializers.stock import StockSerializer
from common_utils.views.mixins import AbstractViewSet
from common_utils.users.permissions import PermissionUtils, CustomPermissionClass
from common_utils.response.mixins import ResponseHandlerMixin
from common_utils.pagination.default_pagination import CustomDefaultPagination
from common_utils.cache.redis_cache import redis_client

from apps.stocks.models import Stock

# Create your views here.

class StockViewSet(AbstractViewSet,ResponseHandlerMixin):
    queryset = Stock.objects.filter()
    serializer_class = StockSerializer
    permission_classes = [CustomPermissionClass]
    pagination_class = CustomDefaultPagination