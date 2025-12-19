from rest_framework import serializers
from common_utils.serializers.base_serializer import DynamicFieldsModelSerializer
from apps.notifications.models import PriceAlert


class PriceAlertSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PriceAlert
        fields = [
            "id",
            "user",
            "stock",
            "alert_type",
            "threshold_value",
            "window_minutes",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
