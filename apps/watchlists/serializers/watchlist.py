from apps.watchlists.models import Watchlist
from common_utils.serializers.base_serializer import DynamicFieldsModelSerializer


class WatchlistSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Watchlist
        fields = [
            "id",
            "user",
            "name",
            "is_default",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
