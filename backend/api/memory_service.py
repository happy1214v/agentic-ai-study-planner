from .models import AgentMemory


def get_user_memories(user, limit=5):
    return AgentMemory.objects.filter(
        user=user
    ).order_by("-created_at")[:limit]


def search_relevant_memories(user, task, limit=5):
    """
    Find memories that are relevant to the current task
    using simple keyword matching.
    """

    if not task:
        return []

    words = [
        word.lower().strip(".,!?;:()[]{}")
        for word in task.split()
        if len(word.strip(".,!?;:()[]{}")) >= 3
    ]

    if not words:
        return []

    memories = AgentMemory.objects.filter(
        user=user
    ).order_by("-created_at")

    scored_memories = []

    for memory in memories:
        memory_text = (
            f"{memory.task} {memory.result}"
        ).lower()

        score = sum(
            1 for word in words
            if word in memory_text
        )

        if score > 0:
            scored_memories.append(
                (score, memory)
            )

    scored_memories.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        memory
        for score, memory in scored_memories[:limit]
    ]