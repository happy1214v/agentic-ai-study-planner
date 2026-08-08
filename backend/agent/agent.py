from backend.agent.tools import calculator
from backend.agent.llm import LLM
from backend.agent.planner.planner import Planner
from backend.agent.memory.memory import Memory
from backend.agent.router import TaskRouter


class AIAgent:
    def __init__(self):
        self.name = "Agentic AI"

        self.memory = Memory()
        self.router = TaskRouter()

        self.tools = {
            "calculator": calculator
        }

        self.llm = LLM()
        self.planner = Planner()

    def remember(self, message):
        self.memory.add(message)

    def get_memory(self):
        return self.memory.get_all()

    def think(self, task):
        return self.llm.generate(task)

    def use_tool(self, tool_name, input_data):
        tool = self.tools.get(tool_name)

        if not tool:
            return f"Tool '{tool_name}' not found"

        return tool(input_data)

    def create_plan(self, task):
        return self.planner.create_plan(task)

    def run(self, task):
        self.remember(task)

        task_type = self.router.route(task)

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

        if task_type == "planner":
            plan = self.create_plan(task)

            return {
                "agent": self.name,
                "task": task,
                "type": task_type,
                "plan": plan,
                "status": "completed",
            }

        response = self.think(task)

        return {
            "agent": self.name,
            "task": task,
            "type": task_type,
            "response": response,
            "status": "completed",
        }
    