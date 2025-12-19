from rest_framework import serializers
from common_utils.serializers.base_serializer import DynamicFieldsModelSerializer
from apps.setup.models import CurrencySetup

class CurrencySetupSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CurrencySetup
        fields = [
            "id",
            "currency_code",
            "currency_name",
            "symbol",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

        