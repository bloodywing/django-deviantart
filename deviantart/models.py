from django.db import models
from django.conf import settings

class Token(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                default=None)
    client_id = models.IntegerField(default=0)
    access_token = models.CharField(max_length=50, default=None)
    refresh_token = models.CharField(max_length=40, default=None)
    expires_at = models.DateTimeField(default=None)
