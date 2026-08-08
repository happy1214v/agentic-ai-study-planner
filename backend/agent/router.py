class TaskRouter:

    def route(self, task):
        task_lower = task.lower().strip()

        # Calculator
        calculator_keywords = [
            "calculate",
            "addition",
            "add",
            "sum",
            "subtract",
            "minus",
            "multiply",
            "times",
            "divide",
            "division",
            "plus",
            "minus",
            "product",
        ]

        if any(word in task_lower for word in calculator_keywords):
            return "calculator"

        # Date / Time
        datetime_keywords = [
            "time",
            "date",
            "today",
            "current time",
            "current date",
            "what day",
            "day today",
        ]

        if any(word in task_lower for word in datetime_keywords):
            return "datetime"

        # Planner
        planner_keywords = [
            "plan",
            "planning",
            "schedule",
            "roadmap",
            "steps",
            "study plan",
            "create a plan",
        ]

        if any(word in task_lower for word in planner_keywords):
            return "planner"

        # Default → LLM
        return "llm"