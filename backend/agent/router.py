class TaskRouter:

    def route(self, task):
        task_lower = task.lower()

        if any(word in task_lower for word in [
            "calculate",
            "addition",
            "subtract",
            "multiply",
            "divide"
        ]):
            return "calculator"

        if any(word in task_lower for word in [
            "plan",
            "schedule",
            "roadmap",
            "steps"
        ]):
            return "planner"

        return "llm"
    