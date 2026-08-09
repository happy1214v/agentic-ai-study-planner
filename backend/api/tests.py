from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import AgentMemory


class AgentAPITests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.token = Token.objects.create(
            user=self.user,
        )

        self.client = APIClient()

    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

    def test_agent_requires_authentication(self):
        response = self.client.post(
            "/api/agent/",
            {"task": "Calculate 20 plus 30"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_agent_rejects_missing_task(self):
        self.authenticate()

        response = self.client.post(
            "/api/agent/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    @patch("api.views.AIAgent")
    def test_agent_endpoint(self, mock_agent):
        self.authenticate()

        mock_agent_instance = mock_agent.return_value

        mock_agent_instance.run.return_value = {
            "agent": "Agentic AI",
            "task": "Calculate 20 plus 30",
            "routes": ["calculator"],
            "results": [
                {
                    "type": "calculator",
                    "tool": "calculator",
                    "result": 50,
                }
            ],
            "status": "completed",
        }

        response = self.client.post(
            "/api/agent/",
            {"task": "Calculate 20 plus 30"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["status"],
            "completed",
        )

        self.assertEqual(
            response.data["results"][0]["result"],
            50,
        )

        self.assertEqual(
            AgentMemory.objects.count(),
            1,
        )

    def test_memory_endpoint(self):
        self.authenticate()

        AgentMemory.objects.create(
            user=self.user,
            task="Calculate 40 plus 60",
            result={
                "result": 100,
                "status": "completed",
            },
        )

        response = self.client.get(
            "/api/memory/?limit=10",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["task"],
            "Calculate 40 plus 60",
        )