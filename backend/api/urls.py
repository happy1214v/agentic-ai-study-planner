from django.urls import path

from .views import (
    agent_api,
    memory_api,
    conversation_api,
    register_api,
    login_api,
)


urlpatterns = [
    path(
        "agent/",
        agent_api,
        name="agent-api",
    ),
    path(
        "memory/",
        memory_api,
        name="memory-api",
    ),
    path(
        "conversations/",
        conversation_api,
        name="conversation-api",
    ),
    path(
        "register/",
        register_api,
        name="register-api",
    ),
    path(
        "login/",
        login_api,
        name="login-api",
    ),
]