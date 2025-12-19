import uuid
from django.db import models
from common_utils.models.mixins import BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin
from config import settings

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


class APIKey(BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True, db_index=True, default=uuid.uuid4().hex.upper())

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="api_keys",
        null=True,
        blank=True
    )

    scopes = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        indexes = [
            models.Index(fields=["key"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.owner})"
    


class WebhookSubscription(BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin):
    class EventChoices(models.TextChoices):
        PRICE_UPDATED = "price.updated", "Price Updated"
        ALERT_TRIGGERED = "alert.triggered", "Alert Triggered"


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="webhooks"
    )

    event = models.CharField(max_length=50, choices=EventChoices.choices)

    target_url = models.URLField()
    secret = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)

    failure_count = models.PositiveIntegerField(default=0)
    last_failure_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        unique_together = ("user", "event", "target_url")

    def __str__(self):
        return f"{self.event} -> {self.target_url}"