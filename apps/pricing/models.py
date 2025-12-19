from apps.stocks.models import Stock
from common_utils.models.mixins import BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin
from django.db import models

class StockPrice(BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin):

    stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, related_name="prices")
    price = models.DecimalField(max_digits=20, decimal_places=4)
    source = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["stock", "timestamp"]),
        ]
        ordering = ["-timestamp"]
        constraints = [
            models.UniqueConstraint(
                fields=["stock", "timestamp", "source"],
                name="unique_stock_price_per_source",
            )
        ]

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError("StockPrice records are immutable")
        super().save(*args, **kwargs)


