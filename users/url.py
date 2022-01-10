from django.urls import include, path

from users.api_views import *

urlpatterns = [
   path('login', Login.as_view() ),
   path('refresh-token', RefreshToken.as_view() ),
]