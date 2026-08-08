from .models import AgentMemory


def get_user_memories(user, limit=5):
    return AgentMemory.objects.filter(
        user=user
    ).order_by("-created_at")[:limit]