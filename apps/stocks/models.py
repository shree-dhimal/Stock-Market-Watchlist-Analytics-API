from common_utils.models.mixins import BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin


from django.db import models

class Stock(BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin):
    
    symbol = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    exchange = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["symbol"]),
            models.Index(fields=["exchange"]),
        ]

    def __str__(self):
        return f"{self.symbol} ({self.exchange})"
