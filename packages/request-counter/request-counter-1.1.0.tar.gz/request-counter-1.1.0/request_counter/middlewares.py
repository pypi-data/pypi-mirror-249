"""request counter middleware"""
import redis
from django.conf import settings


class APICounterMiddleware:
    """api counter to store in redis"""

    API_START_PATH = getattr(settings, "API_START_PATH", "/api/")

    def __init__(self, get_response):
        self.get_response = get_response
        url = getattr(settings, "REDIS_URL", "redis://localhost:6379/7")
        # Adjust connection settings
        self.redis_client = redis.from_url(url)

    def __call__(self, request):
        # Modify this path to match your API endpoints
        if request.path.startswith(self.API_START_PATH):
            self.increment_request_count(request.path)
        response = self.get_response(request)
        return response

    def increment_request_count(self, path):
        """Increment request count in Redis"""
        path_key = f"api_request_count:{path}"
        current_count = self.redis_client.get(path_key)
        if current_count is None:
            current_count = 0
        else:
            current_count = int(current_count)
        self.redis_client.set(path_key, current_count + 1)
