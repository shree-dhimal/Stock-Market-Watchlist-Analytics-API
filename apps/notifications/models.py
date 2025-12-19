from common_utils.models.mixins import BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin
from django.db import models
from django.conf import settings
from apps.stocks.models import Stock

# Create your models here.
class PriceAlert(BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin):
    class AlertType(models.TextChoices):
        ABOVE = "above", "Price Above"
        BELOW = "below", "Price Below"
        PERCENT_CHANGE = "percent_change", "Percent Change"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="price_alerts")
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING, related_name="price_alerts")

    alert_type = models.CharField(max_length=20, choices=AlertType.choices, default=AlertType.PERCENT_CHANGE)
    threshold_value = models.DecimalField(max_digits=20, decimal_places=4)
    window_minutes = models.PositiveIntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.stock} - {self.alert_type}"
    


class Notification(BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)