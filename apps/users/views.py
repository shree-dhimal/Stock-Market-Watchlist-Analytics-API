from django.shortcuts import render

# Create your views here.
import traceback
from common_utils.users import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from django.conf import settings
from common_utils.response.mixins import ResponseHandlerMixin
from common_utils.views.mixins import AbstractViewSet
from common_utils.users.permissions import PermissionUtils, CustomPermissionClass, IsSuperUser
from common_utils.pagination.default_pagination import CustomDefaultPagination
from common_utils.cache.redis_cache import get_redis_client
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated


from apps.users.models import  Users
from apps.users.serializers.authentication import CustomTokenObtainPairSerializer
from apps.users.serializers.users import CreateUsersSerializer, GetUserSelfApiSerializer, GetGroupsSerializer
from decouple import config
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.contrib.auth.models import  Group, Permission


class UserViewSet(AbstractViewSet):
    queryset = Users.objects.all()
    serializer_class = CreateUsersSerializer
    permission_classes = [CustomPermissionClass]
    pagination_class = CustomDefaultPagination


class UserLoginView(ResponseHandlerMixin, TokenObtainPairView, ):
    '''
    View to handle user login and JWT token generation.
    Sets JWT tokens in HttpOnly cookies upon successful authentication.
    
    '''
    permission_classes = [AllowAny]
    authentication_classes = ()
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return self.exception_response(e)
        try:
            # user = authenticate(
            #     request,
            #     username=request.data.get("username"),
            #     password=request.data.get("password"),
            # )
            tokens = serializer.validated_data
            access_token = tokens.get("access")
            refresh_token = tokens.get("refresh")
            access_token_expiry = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
            refresh_token_expiry = settings.SIMPLE_JWT[
                "REFRESH_TOKEN_LIFETIME"
            ].total_seconds()
            cookie_domain = config("COOKIE_DOMAIN", default=None)

            if isinstance(settings.DEBUG, bool) and settings.DEBUG:
                secure_status = False
                response = self.success_response(data=[{"access": access_token, "refresh": refresh_token}], message="Login successful", status=status.HTTP_200_OK)
            else:
                secure_status = True
                response = self.success_response()
            response.set_cookie(
                domain=cookie_domain,
                key=settings.JWT_ACCESS,
                value=access_token,
                max_age=access_token_expiry,
                httponly=True,
                secure=secure_status,
                # samesite="Lax",
            )
            response.set_cookie(
                domain=cookie_domain,
                key=settings.JWT_REFRESH,
                value=refresh_token,
                max_age=refresh_token_expiry,
                httponly=True,
                secure=secure_status,
                # samesite="Lax",
                
            )
            return response
        except Exception as e:
            return self.exception_response(e)


class UserLogoutView(ResponseHandlerMixin, APIView):
    '''
    View to handle user logout and JWT token blacklisting.
    Deletes JWT tokens from HttpOnly cookies upon logout.

    '''

    def _delete_cookie(self, response, cookie_name, domain=None, samesite=None):
        response.delete_cookie(
            key=cookie_name,
            path="/",
            domain=domain,
            samesite=samesite,
        )

    def post(self, request, *args, **kwargs):
        try:

            refresh_token = request.COOKIES.get(settings.JWT_REFRESH) or request.data.get("refresh_token")
            access_token = request.COOKIES.get(settings.JWT_ACCESS) or request.data.get("access_token")

            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except TokenError:
                    pass  # already invalid or expired

            cookies_to_delete = {
                settings.JWT_ACCESS: {"samesite": "Lax"},
                settings.JWT_REFRESH: {"samesite": "Lax"},
                "csrftoken": {},
                "sessionid": {},
            }

            cookie_domain = config("COOKIE_DOMAIN", default=None)

            response = self.success_response(
                message="Logged out successfully",
                status=status.HTTP_200_OK,
            )

            for cookie, options in cookies_to_delete.items():
                if cookie in request.COOKIES:
                    self._delete_cookie(
                        response,
                        cookie,
                        domain=cookie_domain,
                        samesite=options.get("samesite"),
                    )

            return response

        except Exception as e:
            traceback.print_exc()
            return self.exception_response(e)
        

class GetAllPermissionsView(ResponseHandlerMixin, APIView):
    '''
    View to get all available permissions of the system.
    permission code = method_modelname

    response: {"ModelName": [{id:,name:,code:"permission_code1"},{id:,name:,code:"permission_code1"}, ...]}
    '''
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        try:
            permissions = PermissionUtils.get_all_permissions()
            
            return self.success_response(
                data=permissions,
                message="User permissions fetched successfully",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return self.exception_response(e)

class GetAllGroupsView(ResponseHandlerMixin, APIView):
    '''
    View to get all available groups and their permissions in the system.
    '''
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        try:
            groups_permissions = PermissionUtils.get_all_groups(**kwargs)
            if not kwargs.get('id'):
                
                serializer = GetGroupsSerializer(groups_permissions, many=True, fields =['id', 'name'])
            else:
                serializer = GetGroupsSerializer(groups_permissions.first(), fields =['id', 'name', 'permissions'])
            return self.success_response(
                data=serializer.data,
                message="Groups Retrieved successfully",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return self.exception_response(e) 


class CreateGroupsPermissionsView(ResponseHandlerMixin, APIView):
    '''
    View to create groups and assign permissions to them.
    '''
    permission_classes = [IsSuperUser]

    def post(self, request, *args, **kwargs):
        try:
            group_name = request.data.get("group_name")
            permissions = request.data.get("permissions", [])
            app_label = request.data.get("app_label", None)
            replace = request.data.get("replace", True)
            
            if not group_name:
                return self.error_response(
                    message="Group name is required",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            created_group = PermissionUtils.create_group_with_permissions(
                group_name=group_name,
                permission_codenames=permissions,
                app_label=app_label,
                replace=replace,
            )
            if not created_group:
                return self.error_response(
                    message="Role could not be created",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            
            return self.success_response(
                data=[],
                message="Role created successfully",
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return self.exception_response(e)
        
class AssignGroupUserView(ResponseHandlerMixin, APIView):
    '''
    View to assign groups (roles) to a user.
    '''
    permission_classes = [IsSuperUser]

    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get("user")
            groups_name = request.data.get("groups_names", [])
            
            if not user_id or not groups_name:
                return self.error_response(
                    message="User ID and group name are required",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user_instance = Users.objects.filter(id=user_id).first()
            if not user_instance:
                return self.error_response(
                    message="User does not exist",
                    status=status.HTTP_404_NOT_FOUND,
                )
            groups_id = Group.objects.filter(name__in=groups_name).values_list('id', flat=True)
            
            if not groups_id:
                return self.error_response(
                    message="Group does not exist",
                    status=status.HTTP_404_NOT_FOUND,
                )
            result = PermissionUtils.assign_group_to_user(
                user=user_instance,
                groups_id=groups_id,
            )
            
            return self.success_response(
                data={"result": result},
                message="Role assigned to user successfully",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return self.exception_response(e)


class GetUserSelfView(ResponseHandlerMixin, APIView):
    '''
    View to get the details of the currently authenticated user.
    '''
    # extra_permissions = ["view_users"]

    permission_classes = [IsAuthenticated, CustomPermissionClass]

    def get(self, request, *args, **kwargs):
        try:
            user_instance = request.user
            serializer = GetUserSelfApiSerializer(user_instance, partial =True)
            return self.success_response(
                data=serializer.data,
                message="User details fetched successfully",
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return self.exception_response(e)