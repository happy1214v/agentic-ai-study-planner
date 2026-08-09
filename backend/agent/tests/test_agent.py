from django.test import SimpleTestCase

from agent.agent import AIAgent


class AIAgentTests(SimpleTestCase):

    def setUp(self):
        self.agent = AIAgent()

    def test_calculator_task(self):
        result = self.agent.run(
            "Calculate 25 multiplied by 4"
        )

        self.assertEqual(
            result["status"],
            "completed",
        )

        self.assertIn(
            "calculator",
            result["routes"],
        )

        calculator_result = result["results"][0]

        self.assertEqual(
            calculator_result["result"],
            100,
        )

    def test_datetime_task(self):
        result = self.agent.run(
            "What is the current date and time?"
        )

        self.assertEqual(
            result["status"],
            "completed",
        )

        self.assertIn(
            "datetime",
            result["routes"],
        )

    def test_planner_task(self):
        result = self.agent.run(
            "Create a study plan to learn Python"
        )

        self.assertEqual(
            result["status"],
            "completed",
        )

        self.assertIn(
            "planner",
            result["routes"],
        )

    def test_multi_intent_task(self):
        result = self.agent.run(
            "Calculate 20 plus 30 and explain it"
        )

        self.assertEqual(
            result["status"],
            "completed",
        )

        self.assertEqual(
            result["routes"],
            [
                "calculator",
                "llm",
            ],
        )

        self.assertEqual(
            result["results"][0]["result"],
            50,
        )

        self.assertEqual(
            result["results"][1]["type"],
            "llm",
        )
        