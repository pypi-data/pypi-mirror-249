import redis
from django.conf import settings
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import ApiRequestCounter


class ApiCounterSerializer(serializers.ModelSerializer):
    """api counter serializer"""

    class Meta:
        model = ApiRequestCounter
        fields = ("path", "count", "updated_at")


class Paginator(PageNumberPagination):
    """paginator"""

    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 500


class ApiCounterViewSet(ModelViewSet):
    """api counter view set"""

    permission_classes = [IsAdminUser]
    pagination_class = Paginator
    page_size = 10
    serializer_class = ApiCounterSerializer
    queryset = ApiRequestCounter.objects.all().order_by("-count")

    def delete(self, request, *args, **kwargs):
        """clearing the database record of api counter"""
        self.get_queryset().update(count=0)
        return Response("count reset", status=204)


class RedisCounterViewSet(ModelViewSet):
    """api counter view set"""

    permission_classes = [IsAdminUser]
    URL = url = getattr(settings, "REDIS_URL", "redis://localhost:6379/7")

    def get(self, *args, **kwargs):
        """get api view for redis view"""
        redis_client = redis.from_url(self.URL)
        keys = redis_client.keys("api_request_count:*")
        data = []
        for key in keys:
            data.append(
                {
                    "path": key.decode("utf-8").split(":")[-1],
                    "count": int(redis_client.get(key) or 0),
                }
            )

        return Response(data)

    def delete(self, *args, **kwargs):
        """clearing the redis record of api counter"""
        redis_client = redis.from_url(self.URL)
        keys = redis_client.keys("api_request_count:*")
        for key in keys:
            redis_client.delete(key, 0)
        return Response("Redis count reset", status=204)
