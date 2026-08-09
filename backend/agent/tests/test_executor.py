from django.test import SimpleTestCase

from agent.executor import Executor


class ExecutorTests(SimpleTestCase):

    def setUp(self):
        self.executor = Executor(max_retries=2)

    def test_execute_valid_plan(self):
        result = self.executor.execute(
            [
                "Step one",
                "Step two",
            ]
        )

        self.assertEqual(
            result["status"],
            "completed",
        )

        self.assertEqual(
            len(result["results"]),
            2,
        )

    def test_valid_step_completed(self):
        result = self.executor.execute(
            ["Valid step"]
        )

        step_result = result["results"][0]

        self.assertEqual(
            step_result["status"],
            "completed",
        )

        self.assertEqual(
            step_result["attempts"],
            1,
        )

    def test_empty_step_retries(self):
        result = self.executor.execute(
            [""]
        )

        step_result = result["results"][0]

        self.assertEqual(
            step_result["status"],
            "failed",
        )

        self.assertEqual(
            step_result["attempts"],
            3,
        )

    def test_empty_plan(self):
        result = self.executor.execute([])

        self.assertEqual(
            result["status"],
            "failed",
        )

        self.assertEqual(
            result["results"],
            [],
        )
        