class TaskRouter:

    def route(self, task):
        task_lower = task.lower()

        # Calculator
        if any(word in task_lower for word in [
            "calculate",
            "addition",
            "subtract",
            "multiply",
            "divide"
        ]):
            return "calculator"

        # Date / Time
        if any(word in task_lower for word in [
            "time",
            "date",
            "today",
            "current time",
            "current date"
        ]):
            return "datetime"

        # Planner
        if any(word in task_lower for word in [
            "plan",
            "schedule",
            "roadmap",
            "steps"
        ]):
            return "planner"

        # Default
        return "llm"
    