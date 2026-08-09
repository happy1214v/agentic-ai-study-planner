from .tools import calculator, datetime_tool
from .llm import LLM
from .planner.planner import Planner
from .memory.memory import Memory
from .router import TaskRouter
from .executor import Executor


class AIAgent:
    def __init__(self):
        self.name = "Agentic AI"

        self.memory = Memory()
        self.router = TaskRouter()
        self.planner = Planner()
        self.executor = Executor()

        self.tools = {
            "calculator": calculator,
            "datetime": datetime_tool,
        }

        self.llm = LLM()

    def remember(self, message):
        self.memory.add(message)

    def get_memory(self):
        return self.memory.get_all()

    def search_memory(self, keyword):
        return self.memory.search(keyword)

    def think(self, task):
        return self.llm.generate(task)

    def use_tool(self, tool_name, input_data):
        tool = self.tools.get(tool_name)

        if not tool:
            return f"Tool '{tool_name}' not found"

        if tool_name == "datetime":
            return tool()

        return tool(input_data)

    def create_plan(self, task):
        return self.planner.create_plan(task)

    def execute_plan(self, plan):
        return self.executor.execute(plan)

    def explain_result(self, task, result):
        prompt = (
            f"Original task: {task}\n"
            f"Calculated result: {result}\n\n"
            "Explain the calculated result clearly in simple words."
        )

        return self.think(prompt)

    def run(self, task, context=None):
        self.remember(task)

        routes = self.router.route_multiple(task)

        results = []

        for route in routes:

            # Calculator
            if route == "calculator":
                result = self.use_tool(
                    "calculator",
                    task,
                )

                results.append({
                    "type": "calculator",
                    "tool": "calculator",
                    "result": result,
                })

            # Date / Time
            elif route == "datetime":
                result = self.use_tool(
                    "datetime",
                    None,
                )

                results.append({
                    "type": "datetime",
                    "tool": "datetime",
                    "result": result,
                })

            # Planner
            elif route == "planner":
                plan = self.create_plan(task)
                execution = self.execute_plan(plan)

                results.append({
                    "type": "planner",
                    "plan": plan,
                    "execution": execution,
                })

            # LLM
            elif route == "llm":
                llm_task = task

                if results:
                    previous_results = "\n".join(
                        [
                            f"{item['type']}: {item.get('result', item.get('execution', item.get('plan', '')))}"
                            for item in results
                        ]
                    )

                    llm_task = (
                        f"Current task: {task}\n\n"
                        f"Results from previous actions:\n"
                        f"{previous_results}\n\n"
                        "Use these results to answer or explain the task clearly."
                    )

                elif context:
                    context_text = "\n".join(
                        [
                            f"Previous task: {item['task']}\n"
                            f"Previous result: {item['result']}"
                            for item in context
                        ]
                    )

                    llm_task = (
                        f"Previous conversation context:\n"
                        f"{context_text}\n\n"
                        f"Current task: {task}"
                    )

                response = self.think(llm_task)

                if isinstance(response, str) and response.startswith(
                    "LLM error:"
                ):
                    results.append({
                        "type": "llm",
                        "error": response,
                    })
                else:
                    results.append({
                        "type": "llm",
                        "response": response,
                    })

        failed = any(
            "error" in item
            for item in results
        )

        return {
            "agent": self.name,
            "task": task,
            "routes": routes,
            "results": results,
            "status": "failed" if failed else "completed",
        }