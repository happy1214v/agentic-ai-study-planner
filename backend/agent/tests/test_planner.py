from django.test import SimpleTestCase

from agent.planner.planner import Planner


class PlannerTests(SimpleTestCase):

    def setUp(self):
        self.planner = Planner()

    def test_study_plan(self):
        plan = self.planner.create_plan(
            "Create a study plan to learn Python"
        )

        self.assertGreater(
            len(plan),
            0,
        )

        self.assertIn(
            "Define study goals",
            plan,
        )

    def test_website_plan(self):
        plan = self.planner.create_plan(
            "Create a website"
        )

        self.assertIn(
            "Build the backend",
            plan,
        )

    def test_project_plan(self):
        plan = self.planner.create_plan(
            "Create a software project"
        )

        self.assertGreater(
            len(plan),
            0,
        )

    def test_generic_plan(self):
        plan = self.planner.create_plan(
            "Complete this task"
        )

        self.assertEqual(
            len(plan),
            5,
        )