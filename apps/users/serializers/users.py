from common_utils.serializers.base_serializer import DynamicFieldsModelSerializer, BaseAuditSerializer
from rest_framework import serializers

from apps.users.models import Users
from django.contrib.auth.models import Group, Permission

class CreateUsersSerializer(DynamicFieldsModelSerializer):    
    """
    Serializer for the Users model.
    Inherits from DynamicFieldsModelSerializer to allow dynamic field selection.
    """
    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'phone',
            'account_tier',
            'preferred_currency',
        ]
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password) 
        user.save()
        return user

class CreatePermissionSerializer(DynamicFieldsModelSerializer):
    """
    Serializer for the Permission model.
    Inherits from DynamicFieldsModelSerializer to allow dynamic field selection.
    """
    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'codename',
            'content_type',
        ]
class CreateRoleSerializer(DynamicFieldsModelSerializer):
    """
    Serializer for the Users model including roles (groups and permissions).
    Inherits from DynamicFieldsModelSerializer to allow dynamic field selection.
    """
    permissions = CreatePermissionSerializer(many=True, fields =['id', 'name', 'codename'])
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'permissions',
        ]

class GetUserSelfApiSerializer(DynamicFieldsModelSerializer):
    """
    Serializer for fetching user details along with roles and permissions.
    Inherits from DynamicFieldsModelSerializer to allow dynamic field selection.
    """
    roles = CreateRoleSerializer(many=True, source='groups', fields =['id', 'name'])
    permissions = serializers.SerializerMethodField()
    account_tier = serializers.SerializerMethodField(source='account_tier_account_type')
    preferred_currency = serializers.SerializerMethodField(source='preferred_currency_currency_code')

    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'full_name',
            'email',
            'phone',
            'is_superuser'
            'account_tier',
            'preferred_currency',
            'roles',
            'permissions',
        ]

    def get_permissions(self, obj):
        if obj.is_superuser:
            return list(Permission.objects.values_list("codename", flat=True))

        user_roles = obj.groups.all()
        user_permissions = (
            Permission.objects.filter(group__in=user_roles) |
            Permission.objects.filter(user=obj)
        ).distinct()

        return list(user_permissions.values_list("codename", flat=True))
    


class GetGroupsSerializer(DynamicFieldsModelSerializer):
    """
    Serializer for fetching group details along with permissions.
    Inherits from DynamicFieldsModelSerializer to allow dynamic field selection.
    """
    permissions = CreatePermissionSerializer(many=True, fields =['id', 'name', 'codename'])
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'permissions',
        ]
