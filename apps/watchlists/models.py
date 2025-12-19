from apps.stocks.models import Stock
from common_utils.models.mixins import BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin
from apps.users.models import  Users
from django.db import models

class Watchlist(BaseAuditModelMixin, BaseTimeStampModelMixin, SoftDeleteModelMixin):
    user = models.ForeignKey(
        Users, on_delete=models.DO_NOTHING, related_name="watchlists"
    )
    name = models.CharField(max_length=255, help_text="Name of the watchlist")
    is_default = models.BooleanField(default=False, help_text="Is this the default watchlist?")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the watchlist was created")

    class Meta:
        unique_together = ("user", "name")

    def __str__(self):
        return f"{self.name} ({self.user})"
    

class WatchlistItem(models.Model):
    watchlist = models.ForeignKey(
        Watchlist, on_delete=models.DO_NOTHING, related_name="items"
    )
    stock = models.ForeignKey(Stock, on_delete=models.DO_NOTHING, related_name="watchlists")

    alert_thresholds = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("watchlist", "stock")
        indexes = [
            models.Index(fields=["watchlist", "stock"]),
        ]

    def __str__(self):
        return f"{self.stock.symbol} in {self.watchlist.name}"