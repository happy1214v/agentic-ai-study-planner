from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import AgentRequestSerializer, AgentMemorySerializer
from .models import AgentMemory
from .memory_service import get_user_memories, search_relevant_memories
from agent.agent import AIAgent
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import (
    AgentRequestSerializer,
    AgentMemorySerializer,
    RegisterSerializer,
)


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

        previous_memories = search_relevant_memories(
            request.user,
            task,
            limit=5,
        )

        context = [
            {
                "task": memory.task,
                "result": memory.result,
            }
            for memory in previous_memories
        ]

        result = agent.run(
            task,
            context=context,
        )

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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def memory_api(request):
    try:
        limit = int(request.GET.get("limit", 5))

        if limit < 1:
            limit = 5

        if limit > 50:
            limit = 50

        memories = get_user_memories(
            request.user,
            limit=limit,
        )

        serializer = AgentMemorySerializer(
            memories,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    except ValueError:
        return Response(
            {"error": "limit must be a number"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def conversation_api(request):
    memories = get_user_memories(
        request.user,
        limit=50,
    )

    conversations = []

    for memory in memories:
        conversations.append({
            "id": memory.id,
            "task": memory.task,
            "result": memory.result,
            "created_at": memory.created_at,
        })

    return Response(
        conversations,
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = serializer.save()

    token, _ = Token.objects.get_or_create(
        user=user
    )

    return Response(
        {
            "message": "Registration successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "token": token.key,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {
                "error": "Username and password are required."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(
        username=username,
        password=password,
    )

    if user is None:
        return Response(
            {
                "error": "Invalid username or password."
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(
        user=user
    )

    return Response(
        {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "token": token.key,
        },
        status=status.HTTP_200_OK,
    )