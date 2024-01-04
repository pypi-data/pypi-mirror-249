"""models to store data to database"""
from django.db import models


class ApiRequestCounter(models.Model):
    """api counter model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    path = models.CharField(max_length=200, primary_key=True)
    count = models.BigIntegerField(default=0)

    class Meta:
        db_table = "api_request_counter"
