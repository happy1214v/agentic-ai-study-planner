from django.urls import path

from .views import agent_api, memory_api

urlpatterns = [
    path("agent/", agent_api, name="agent-api"),
    path("memory/", memory_api, name="memory-api"),
]