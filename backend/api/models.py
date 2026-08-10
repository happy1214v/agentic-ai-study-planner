from django.db import models
from django.contrib.auth.models import User


class AgentMemory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="agent_memories",
    )

    task = models.TextField()

    result = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.user.username} - {self.task}"