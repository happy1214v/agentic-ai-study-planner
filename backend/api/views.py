from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import AgentRequestSerializer
from .models import AgentMemory
from agent.agent import AIAgent


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def agent_api(request):
    serializer = AgentRequestSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    task = serializer.validated_data["task"]

    try:
        agent = AIAgent()
        result = agent.run(task)

        AgentMemory.objects.create(
            user=request.user,
            task=task,
            result=result,
        )

        return Response(
            result,
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )