from django.urls import include, path

from polls.api_views import *

urlpatterns = [
    path('polls', PollList.as_view()),
]