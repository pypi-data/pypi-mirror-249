
# Django-request-counter

Install this app to get django api request count


## Installation

Install my-project with pip

```bash
  pip install request-counter
```
In settings.py add below
Add the app in installed apps 
```
INSTALLED_APPS = [
    ...
    "request_counter",
]
```
Add middleware
```
MIDDLEWARE = [
    ...
    "request_counter.middlewares.APICounterMiddleware",
]
```
To check using API Add
```
urlpartterns = [
    ...
    path("",include("request_counter.urls")),
]
```
Set Redis Url
```
# REDIS_URL = "redis://localhost:6379/7" # by default
REDIS_URL = "<your redis url path>"
API_START_PATH = "/api/" # by default set "" for monitoring all path
API_START_PATH = "<your starting path>"

```
You need to setup cron to periodically save the data into default database 
```
python manage.py store_api_count
```

Now make api request with admin user
```
curl --location '<base-url>/api-count/' \
--header '<your authentication header>'

curl --location '<base-url>/api-count/redis' \
--header '<your authentication header>'
```