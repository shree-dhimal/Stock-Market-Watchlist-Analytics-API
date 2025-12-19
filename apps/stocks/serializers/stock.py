from apps.stocks.models import Stock
from common_utils.serializers.base_serializer import DynamicFieldsModelSerializer


class StockSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Stock
        fields = [
            "id",
            "symbol",
            "name",
            "exchange",
            "currency",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]