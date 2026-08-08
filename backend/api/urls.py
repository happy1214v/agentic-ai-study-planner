from django.urls import path

from .views import agent_api


urlpatterns = [
    path("agent/", agent_api, name="agent-api"),
]