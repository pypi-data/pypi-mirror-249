from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import ApiRequestCounter

# Create your views here.


class ApiCounterSerializer(serializers.ModelSerializer):
    """api counter serializer"""

    class Meta:
        model = ApiRequestCounter
        fields = ("path", "count", "updated_at")


class Paginator(PageNumberPagination):
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
