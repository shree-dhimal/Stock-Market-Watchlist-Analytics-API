from rest_framework import serializers
from common_utils.serializers.base_serializer import DynamicFieldsModelSerializer
from apps.setup.models import APIKey

class APIKeySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = APIKey
        fields = [
            "id",
            "name",
            "key",
            "owner",
            "scopes",
            "is_active",
            "last_used_at",
            "expires_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]