from rest_framework import serializers
from common_utils.serializers.base_serializer import DynamicFieldsModelSerializer
from apps.setup.models import AccountsTypeSetup

class AccountsTypeSetupSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = AccountsTypeSetup
        fields = [
            "id",
            "account_type",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]