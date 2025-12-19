from collections import defaultdict
from common_utils.cache.redis_cache import get_redis_client
from django.contrib.auth.models import  Group, Permission
from django.contrib.auth.models import AnonymousUser

from django.urls import resolve
from rest_framework.permissions import BasePermission 
from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from django.core.exceptions import ValidationError

class PermissionUtils:
    '''
    Utility class for handling user permissions based on groups and caching.
    Models used: User, Group, Permission (django default models)
    :param
    :user : User instance
    :model : Django Model class()
    :view : View instance
    :request : Request instance

    Usage:
        permission_utils = PermissionUtils(user=request.user, model=SomeModel)
        has_perm = permission_utils.has_permission('view')

        django saves the permissions in the format by default: 'action_modelname'
        where action can be: 'view', 'add', 'change', 'delete' + additional permissions if any comes from views.
    '''
    def __init__(self, user = None, model_name=None, view=None, request=None, extra_permissions=None):
        self.user = user
        self.model_name = model_name.lower() if model_name else model_name
        self.view = view
        self.request = request
        self.actions = {
            'view': 'List',
            'add': 'Create',
            'change': 'Edit',
            'delete': 'Delete'
        }
        self.action_css_classes = {
            'List': "",
            'Create': "",
            'Edit': "text-blue-600",
            'Delete': "text-red-600"
        }
        self.extra_permissions =  extra_permissions if extra_permissions else []

        self.exclude_actions = getattr(self.view, "exclude_actions", ["List","Create"])

    @staticmethod  
    def format_action(value, css_class=""):
        data = {
            "name": value,
            "emit": f"on{value.replace(' ', '')}",
        }
        if css_class:
            data["class"] = css_class
        return data
    
    def has_permission(self, action):
        '''
        Check if the user has the required permission for the given action on the model.
        Uses cache to reduce DB queries.

        :param action: 'view', 'add', 'change', 'delete'
        :return: Boolean
        '''
        if action not in self.actions.keys():
            raise ValueError(f"Invalid action: {action}. Valid actions are: {list(self.actions.keys())}")

        # Superuser always has permission
        # if self.user.is_superuser:
        #     return True

        # Create a cache key based on user id, model name, and action

        try:
            cache_key = f"user_perm:{self.user.id}:{self.view.request.path}:{action}"
            # Try to get cached result
            cached_result = get_redis_client("default").get(cache_key)
        except Exception as e:
            cached_result = None
            
        # cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        # Check group permissions
        user_groups = self.user.groups.all()
        required_permissions = [f'{action}_{self.model_name}'.lower()] if self.model_name else []

        if self.extra_permissions:
            required_permissions.extend(
                [perm.lower() for perm in self.extra_permissions]
            )

        has_perm = False
        for group in user_groups:
            group_perm_codenames = set(group.permissions.values_list('codename', flat=True))
            if all(perm in group_perm_codenames for perm in required_permissions):
                has_perm = True
                break
        try:
            # Cache the result for future use
            get_redis_client("default").set(cache_key, has_perm, ttl=300)  # 300 seconds = 5 minutes
        except Exception as e:
            pass
        
        return has_perm
    
    def get_user_all_permissions(self):
        '''
        Get all permissions for the given user.
        :param user: User instance
        :return: Set of permission codenames
        '''
        if self.user.is_superuser:
            return set(Permission.objects.values_list('codename', flat=True))
        
        user_groups = self.user.groups.all()
        permissions = set()
        for group in user_groups:
            group_permissions = group.permissions.values_list('codename', flat=True)
            permissions.update(group_permissions)
        return permissions
    
    def user_available_actions(self):
        '''
        Get all available actions for the user on the model.
        :return: List of actions
        '''
        available_actions = []
        for key, value in self.actions.items():
            if self.has_permission(key):
                available_actions.append(self.format_action(value, self.action_css_classes[value]))
        exclude_lower = [ex.lower() for ex in self.exclude_actions]
        available_actions = [
            action for action in available_actions
            if action["name"].lower() not in exclude_lower
        ]
        return available_actions

    def get_user_model_permissions(self):
        '''
        Get all permissions for the user related to the model.
        :return: Set of permission codenames
        '''
        if self.user.is_superuser:
            return set(Permission.objects.filter(content_type__model=self.model_name).values_list('codename', flat=True))
        
        user_groups = self.user.groups.all()
        permissions = set()
        for group in user_groups:
            group_permissions = group.permissions.filter(content_type__model=self.model_name).values_list('codename', flat=True)
            permissions.update(group_permissions)
        return permissions
    
    @staticmethod
    def get_all_permissions():
        '''
        Get all permissions grouped by model name.
        :return: dict
        '''
        if get_redis_client("default") is not None:
            cache_key = "all_permissions_dict"
            try:
                cached_permissions = get_redis_client("default").get(cache_key)
                if cached_permissions is not None:
                    return cached_permissions
            except Exception as e:
                pass

        permissions = Permission.objects.select_related(
            "content_type"
        ).values(
            "id",
            "name",
            "codename",
            "content_type__model",
        )

        result = defaultdict(list)

        for perm in permissions:
            model_name = perm["content_type__model"]

            result[model_name].append({
                "id": perm["id"],
                "name": perm["name"],
                "code": perm["codename"],
            })
        cache_key = "all_permissions_dict"
        try:
            get_redis_client("default").set(cache_key, dict(result), ttl=3600)  # Cache for 1 hour
        except Exception as e:
            pass


        return dict(result)
    
    @staticmethod
    def get_all_groups(**kwargs):
        '''
        Get all groups with their permissions.
        :return: dict
        '''
        if get_redis_client("default") is not None:
            if len(kwargs) == 0:
                cache_key = "all_groups_dict"
            else:
                cache_key = "filtered_groups_dict_" + "_".join(f"{k}_{v}" for k, v in kwargs.items())
            try:
                cached_groups = get_redis_client("default").get(cache_key)
                if cached_groups is not None:
                    return cached_groups
            except Exception as e:
                pass

        groups = Group.objects.prefetch_related("permissions").filter(**kwargs)

        # result = []

        # for group in groups:
        #     perms = group.permissions.select_related(
        #         "content_type"
        #     ).values(
        #         "id",
        #         "name",
        #         "codename",
        #         "content_type__model",
        #     )

        #     perm_list = []
        #     for perm in perms:
        #         perm_list.append({
        #             "id": perm["id"],
        #             "name": perm["name"],
        #             "code": perm["codename"],
        #             "model": perm["content_type__model"],
        #         })

        #     result.append({
        #         "id": group.id,
        #         "name": group.name,
        #         "permissions": perm_list,
        #     })
        
        # cache_key = "all_groups_dict"
        # try:
        #     get_redis_client("default").set(cache_key, result, ttl=3600)  # Cache for 1 hour
        # except Exception as e:
        #     pass

        return groups
    
    @staticmethod
    @transaction.atomic
    def create_group_with_permissions(
        group_name,
        permission_codenames,
        app_label=None,
        replace=True,
    ):
        """
        Create or update a group with specified permissions.

        :param group_name: str
        :param permission_codenames: list[str]
        :param app_label: optional Django app label (recommended)
        :param replace: if True, replaces existing permissions; else adds
        :return: Group
        """

        group, _ = Group.objects.get_or_create(name=group_name)

        permission_qs = Permission.objects.filter(
            codename__in=permission_codenames
        )

        if app_label:
            permission_qs = permission_qs.filter(
                content_type__app_label=app_label
            )

        found = set(permission_qs.values_list("codename", flat=True))
        missing = set(permission_codenames) - found

        if missing:
            raise ValidationError(
                f"Invalid permission codenames: {', '.join(missing)}, Please Add valid permission codenames."
            )

        if replace:
            group.permissions.set(permission_qs)
        else:
            group.permissions.add(*permission_qs)

        return group

    @staticmethod   
    def assign_group_to_user(user, groups_id):
        '''
        Assign a group to the user.
        :param group_name: Name of the group
        '''
        try:
            user.groups.clear()
            user.groups.set(groups_id)
            user.save()
            return user.groups.all().values_list('name', flat=True)
        except Group.DoesNotExist:
            raise ValueError(f"Group '{groups_id}' does not exist.")
    
class CustomPermissionClass(BasePermission):
    '''
    Custom permission class to check user permissions based on action and model.
    Usage:
        - permission_classes = [CustomPermissionClass]
        - permissions = {
            'all': 'user-module',
            'list': 'can_view_user-module',
            'create': 'can_add_user-module',
            'update': 'can_update_user-module',
            'delete': 'can_delete_user-module',
          }
    '''
    def has_permission(self, request, view):
        try:
            extra_permissions = getattr(view, "extra_permissions", [])
            method_action = {
                "GET": "view",
                "POST": "add",
                "PUT": "change",
                "PATCH": "change",
                "DELETE": "delete",
            }
            if not request.user or isinstance(request.user, AnonymousUser):
                return False
            if request.method in ["OPTIONS", "HEAD"]:
                return True
            user = request.user
            
            # if user.is_superuser:
            #     return True
            
            if hasattr(view, "get_queryset"):
                model = view.get_queryset().model._meta.model_name
            elif hasattr(view, "queryset") and view.queryset is not None:
                model = view.queryset.model._meta.model_name
            else:
                model = None
            
            permission_utils = PermissionUtils(user=user, model_name=model, view=view, request=request, extra_permissions=extra_permissions)
        
            # Map HTTP methods to action keys
            action_key = method_action.get(request.method.upper())

            if not action_key:
                return False
            
            has_module_permission = permission_utils.has_permission(action_key)

            return bool(has_module_permission)
        
        except ImproperlyConfigured as e:
            raise e
        except Exception as e:
            raise e
            # return False

class IsSuperUser(BasePermission):
    '''
    Custom permission class to allow only superusers.
    Usage:
        - permission_classes = [IsSuperUser]
    '''
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_superuser
    
