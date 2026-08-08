from rest_framework import serializers


class AgentRequestSerializer(serializers.Serializer):
    task = serializers.CharField(
        required=True,
        allow_blank=False
    )