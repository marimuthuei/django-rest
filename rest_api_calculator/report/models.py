from django.db import models
from django.conf import settings
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class APIRequestLog(models.Model):
    api_name = models.CharField(max_length=200, db_index=True, verbose_name="API Name")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             blank=True, related_name="api_users")
    requested_at = models.DateTimeField(db_index=True)
    latency = models.PositiveIntegerField(default=0)
    errors = models.TextField(null=True, blank=True)
    status_code = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.api_name
