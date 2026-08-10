import re


class Planner:

    def _get_requested_steps(self, task):
        match = re.search(
            r"\b(\d+)\s*(?:step|steps|stage|stages)\b",
            task.lower(),
        )

        if match:
            return int(match.group(1))

        return None

    def _fit_steps(self, steps, requested):
        if requested is None:
            return steps

        if requested <= len(steps):
            return steps[:requested]

        while len(steps) < requested:
            steps.append(
                f"Continue with step {len(steps) + 1}"
            )

        return steps[:requested]

    def create_plan(self, task):
        task_lower = task.lower()
        requested = self._get_requested_steps(task)

        if "study" in task_lower or "learn" in task_lower:
            steps = [
                "Define study goals",
                "Break the subject into topics",
                "Learn the fundamentals",
                "Practice with examples",
                "Create a daily study schedule",
                "Work on exercises and projects",
                "Review and revise the topics",
                "Test your knowledge",
                "Identify weak areas",
                "Review progress",
            ]

            return self._fit_steps(steps, requested)

        if "website" in task_lower or "web" in task_lower:
            steps = [
                "Define website requirements",
                "Design the system architecture",
                "Design the user interface",
                "Build the backend",
                "Build the frontend",
                "Connect frontend and backend",
                "Test the application",
                "Fix bugs and improve the application",
                "Deploy the application",
                "Monitor and maintain the website",
            ]

            return self._fit_steps(steps, requested)

        if "project" in task_lower:
            steps = [
                "Define project requirements",
                "Break the project into modules",
                "Design the project architecture",
                "Implement each module",
                "Integrate the modules",
                "Test the project",
                "Fix bugs and improve the project",
                "Review and complete the project",
                "Document the project",
                "Deploy the project",
            ]

            return self._fit_steps(steps, requested)

        steps = [
                f"Understand the task: {task}",
                "Break the task into smaller steps",
                "Execute each step",
                "Check the result",
                "Complete the task",
        ]

        return self._fit_steps(steps, requested)