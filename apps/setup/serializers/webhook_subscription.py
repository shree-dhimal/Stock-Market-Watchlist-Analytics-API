from rest_framework import serializers
from common_utils.serializers.base_serializer import DynamicFieldsModelSerializer
from apps.setup.models import WebhookSubscription

class WebhookSubscriptionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = WebhookSubscription
        fields = [
            "id",
            "user",
            "event",
            "target_url",
            "secret",
            "is_active",
            "failure_count",
            "last_failure_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
