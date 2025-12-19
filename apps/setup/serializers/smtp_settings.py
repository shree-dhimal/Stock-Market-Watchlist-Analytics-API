from rest_framework import serializers
from common_utils.serializers.base_serializer import DynamicFieldsModelSerializer
from apps.setup.models import SMTPSettings

class SMTPSettingsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = SMTPSettings
        fields = [
            "id",
            "smtp_server",
            "port",
            "username",
            "password",
            "use_tls",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
