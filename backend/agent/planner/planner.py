class Planner:

    def create_plan(self, task):
        task_lower = task.lower()

        if "study" in task_lower or "learn" in task_lower:
            return [
                "Define study goals",
                "Break the subject into topics",
                "Create a daily study schedule",
                "Add practice and revision sessions",
                "Review progress"
            ]

        if "website" in task_lower or "web" in task_lower:
            return [
                "Define website requirements",
                "Design the system architecture",
                "Build the backend",
                "Build the frontend",
                "Test the application",
                "Deploy the application"
            ]

        if "project" in task_lower:
            return [
                "Define project requirements",
                "Break the project into modules",
                "Implement each module",
                "Test the project",
                "Review and complete the project"
            ]

        return [
            f"Understand the task: {task}",
            "Break the task into smaller steps",
            "Execute each step",
            "Check the result",
            "Complete the task"
        ]