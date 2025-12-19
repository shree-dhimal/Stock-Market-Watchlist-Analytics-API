from apps.watchlists.models import WatchlistItem
from common_utils.serializers.base_serializer import DynamicFieldsModelSerializer


class WatchlistItemSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = WatchlistItem
        fields = [
            "id",
            "watchlist",
            "stock",
            "alert_thresholds",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
