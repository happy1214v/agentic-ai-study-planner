from .tools import calculator
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
            "calculator": calculator
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

        return tool(input_data)

    def create_plan(self, task):
        return self.planner.create_plan(task)

    def execute_plan(self, plan):
        return self.executor.execute(plan)

    def run(self, task, context=None):
        self.remember(task)

        task_type = self.router.route(task)

        # Calculator task
        if task_type == "calculator":
            result = self.use_tool("calculator", task)

            return {
                "agent": self.name,
                "task": task,
                "type": task_type,
                "tool": "calculator",
                "result": result,
                "status": "completed",
            }

        # Planning task
        if task_type == "planner":
            plan = self.create_plan(task)
            execution = self.execute_plan(plan)

            return {
                "agent": self.name,
                "task": task,
                "type": task_type,
                "plan": plan,
                "execution": execution,
                "status": "completed",
            }

        # LLM task
        llm_task = task

        if context:
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

        return {
            "agent": self.name,
            "task": task,
            "type": task_type,
            "response": response,
            "status": "completed",
        }