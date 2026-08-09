from django.test import SimpleTestCase

from agent.router import TaskRouter


class TaskRouterTests(SimpleTestCase):

    def setUp(self):
        self.router = TaskRouter()

    def test_calculator_route(self):
        result = self.router.route(
            "Calculate 20 plus 30"
        )

        self.assertEqual(
            result,
            "calculator",
        )

    def test_datetime_route(self):
        result = self.router.route(
            "What is the current time?"
        )

        self.assertEqual(
            result,
            "datetime",
        )

    def test_planner_route(self):
        result = self.router.route(
            "Create a study plan for Python"
        )

        self.assertEqual(
            result,
            "planner",
        )

    def test_llm_route(self):
        result = self.router.route(
            "Explain machine learning"
        )

        self.assertEqual(
            result,
            "llm",
        )

    def test_multiple_routes(self):
        result = self.router.route_multiple(
            "Calculate 20 plus 30 and explain it"
        )

        self.assertEqual(
            result,
            ["calculator", "llm"],
        )