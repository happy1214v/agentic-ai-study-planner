from rest_framework import serializers

from .models import AgentMemory


class AgentRequestSerializer(serializers.Serializer):
    task = serializers.CharField(
        required=True,
        allow_blank=False
    )


class AgentMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentMemory
        fields = [
            "id",
            "task",
            "result",
            "created_at",
        ]