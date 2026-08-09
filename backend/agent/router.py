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
            "product",
        ]

        if any(
            word in task_lower
            for word in calculator_keywords
        ):
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

        if any(
            word in task_lower
            for word in datetime_keywords
        ):
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

        if any(
            word in task_lower
            for word in planner_keywords
        ):
            return "planner"

        return "llm"

    def route_multiple(self, task):
        task_lower = task.lower().strip()

        routes = []

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
            "product",
        ]

        datetime_keywords = [
            "time",
            "date",
            "today",
            "current time",
            "current date",
            "what day",
            "day today",
        ]

        planner_keywords = [
            "plan",
            "planning",
            "schedule",
            "roadmap",
            "steps",
            "study plan",
            "create a plan",
        ]

        if any(
            word in task_lower
            for word in calculator_keywords
        ):
            routes.append("calculator")

        if any(
            word in task_lower
            for word in datetime_keywords
        ):
            routes.append("datetime")

        if any(
            word in task_lower
            for word in planner_keywords
        ):
            routes.append("planner")

        if "explain" in task_lower:
            routes.append("llm")

        if not routes:
            routes.append("llm")

        return routes