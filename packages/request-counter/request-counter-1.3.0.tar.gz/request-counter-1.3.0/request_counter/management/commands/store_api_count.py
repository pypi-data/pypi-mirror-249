import redis
from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import ApiRequestCounter

# from your_app.models import APICounts  # Replace 'your_app' with your app name


class Command(BaseCommand):
    help = "Store cumulative API request counts in the database"

    def handle(self, *args, **options):
        url = getattr(settings, "REDIS_URL", "redis://localhost:6379/7")
        # Adjust connection settings
        redis_client = redis.from_url(url)
        keys = redis_client.keys("api_request_count:*")

        for key in keys:
            path = key.decode("utf-8").split(":")[-1]
            count = int(redis_client.get(key) or 0)
            # Assuming you have a model APICounts with fields 'path' and 'count'
            instance, _ = ApiRequestCounter.objects.get_or_create(path=path)
            instance.count += count
            instance.save()
            redis_client.set(key, 0)
        self.stdout.write(self.style.SUCCESS("Stored API counts in the database"))
