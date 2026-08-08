from django.shortcuts import render

# Create your views here.

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from agent.agent import AIAgent


@csrf_exempt
def agent_api(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed"},
            status=405,
        )

    try:
        data = json.loads(request.body)
        task = data.get("task")

        if not task:
            return JsonResponse(
                {"error": "Task is required"},
                status=400,
            )

        agent = AIAgent()
        result = agent.run(task)

        return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500,
        )