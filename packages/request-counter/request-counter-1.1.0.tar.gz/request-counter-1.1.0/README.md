
# Django-request-counter

Install this app to get request count of all the api


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
# REDIS_URL = "redis://localhost:6379/7"
REDIS_URL = "<your redis url path>"
```
You need to setup cron to periodically save the data into database by by default it store data into database
```
python manage.py store_api_count
```

Now make api request with admin user
```
curl --location '<base-url>/api-count' \
--header '<your authentication header>'
```