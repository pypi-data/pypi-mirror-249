from django.urls import path

from . import views

urlpatterns = [
    path(
        "api-count",
        views.ApiCounterViewSet.as_view({"get": "list", "delete": "delete"}),
    )
]
