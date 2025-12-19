
from apps.watchlists.serializers.watchlist import WatchlistSerializer
from apps.watchlists.serializers.watchlistitems import WatchlistItemSerializer
from common_utils.views.mixins import AbstractViewSet
from common_utils.users.permissions import PermissionUtils, CustomPermissionClass
from common_utils.response.mixins import ResponseHandlerMixin
from common_utils.pagination.default_pagination import CustomDefaultPagination
from common_utils.cache.redis_cache import redis_client

from apps.watchlists.models import Watchlist, WatchlistItem

# Create your views here.

class WatchlistViewSet(AbstractViewSet,ResponseHandlerMixin):
    queryset = Watchlist.objects.filter(is_active=True).select_related('user')
    serializer_class = WatchlistSerializer
    permission_classes = [CustomPermissionClass]
    pagination_class = CustomDefaultPagination
    # extra_permissions = [] # Define any extra permissions if needed like {actions}_{model}


class WatchlistItemViewSet(AbstractViewSet,ResponseHandlerMixin):
    queryset = WatchlistItem.objects.filter(is_active=True).select_related('watchlist', 'stock')
    serializer_class = WatchlistItemSerializer
    permission_classes = [CustomPermissionClass]
    pagination_class = CustomDefaultPagination
    # extra_permissions = [] # Define any extra permissions if needed like {actions}_{model}