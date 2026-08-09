import re

from .models import AgentMemory


STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "what",
    "was",
    "were",
    "this",
    "that",
    "from",
    "have",
    "has",
    "our",
    "your",
    "about",
    "please",
    "tell",
    "show",
    "give",
    "does",
    "did",
    "how",
    "why",
    "when",
    "where",
}


def normalize_words(text):
    if not text:
        return []

    words = re.findall(
        r"[a-zA-Z0-9]+",
        text.lower(),
    )

    return [
        word
        for word in words
        if len(word) >= 3
        and word not in STOP_WORDS
    ]


def get_user_memories(user, limit=5):
    return AgentMemory.objects.filter(
        user=user
    ).order_by("-created_at")[:limit]


def search_relevant_memories(user, task, limit=5):
    """
    Find memories relevant to the current task
    using improved keyword scoring.
    """

    if not task:
        return []

    task_words = normalize_words(task)

    if not task_words:
        return []

    memories = AgentMemory.objects.filter(
        user=user
    ).order_by("-created_at")

    scored_memories = []

    for memory in memories:
        memory_task_words = set(
            normalize_words(memory.task)
        )

        memory_result_text = str(
            memory.result
        ).lower()

        memory_result_words = set(
            normalize_words(memory_result_text)
        )

        task_matches = sum(
            1
            for word in task_words
            if word in memory_task_words
        )

        result_matches = sum(
            1
            for word in task_words
            if word in memory_result_words
        )

        score = (
            task_matches * 3
            + result_matches
        )

        if score > 0:
            scored_memories.append(
                (
                    score,
                    memory.created_at,
                    memory,
                )
            )

    scored_memories.sort(
        key=lambda item: (
            item[0],
            item[1],
        ),
        reverse=True,
    )

    return [
        memory
        for score, created_at, memory
        in scored_memories[:limit]
    ]