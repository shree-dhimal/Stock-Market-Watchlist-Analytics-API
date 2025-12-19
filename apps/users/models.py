from apps.setup.models import AccountsTypeSetup, CurrencySetup
from common_utils.models.mixins import BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin
from django.contrib.auth.models import AbstractUser, Group, Permission, AnonymousUser
from django.db import models



class Users(AbstractUser, BaseTimeStampModelMixin, BaseAuditModelMixin, SoftDeleteModelMixin):
    """
    Custom User model extending Django's AbstractUser.
    Includes additional fields and mixins for auditing, timestamping, and soft deletion.
    """
    class Meta:
        db_table = 'auth_user'

        
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    account_tier = models.ForeignKey(AccountsTypeSetup, on_delete=models.DO_NOTHING, null=True, blank=True, help_text="Account tier of the user")
    preferred_currency = models.ForeignKey(CurrencySetup, on_delete=models.DO_NOTHING, null=True, blank=True, help_text="Preferred currency of the user")

    USERNAME_FIELD = 'email'

    @property
    def full_name(self) -> str:
        """
        Returns the user's full name.
        """
        super().get_full_name()
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()





class ErrorLog(BaseTimeStampModelMixin):
    '''
    Model to log server errors occurred
    '''
    error_message = models.TextField()
    model_name = models.CharField(max_length=255, blank=True, null=True)
    api = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Users, null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-created_at']
        db_table = 'errorlog'


class ChangeLog(models.Model):

    '''
    Model to log changes made to other models

    '''

    ACTION_CHOICES = (
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
    )

    user = models.ForeignKey(Users, null=True, blank=True, on_delete=models.DO_NOTHING)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)

    action = models.CharField(
        max_length=10, blank=True, null=True, choices=ACTION_CHOICES
    )
    field = models.CharField(max_length=100, null=True, blank=True)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        db_table = 'changelogs'
