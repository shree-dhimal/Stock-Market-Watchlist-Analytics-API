from django.db import models
from common_utils.models.mixins import BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin

# Create your models here.
class AccountsTypeSetup(BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin):
    '''
    Model to setup different account types eg: premium, gold, silver etc
    '''
    account_type = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['account_type']
        db_table = 'account_types_setup'

class CurrencySetup(BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin):
    '''
    Model to setup different currencies
    '''
    currency_code = models.CharField(max_length=10, unique=True)
    currency_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ['currency_code']
        db_table = 'currency_setup'


class SMTPSettings(BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin):
    '''
    Model to setup SMTP settings for email notifications
    '''
    smtp_server = models.CharField(max_length=255)
    port = models.PositiveIntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    use_tls = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'smtp_settings_setup'