from backend.agent.tools import calculator
from backend.agent.llm import LLM


class AIAgent:
    def __init__(self):
        self.name = "Agentic AI"
        self.memory = []

        self.tools = {
            "calculator": calculator
        }

        self.llm = LLM()

    def remember(self, message):
        self.memory.append(message)

    def think(self, task):
        return self.llm.generate(task)

    def use_tool(self, tool_name, input_data):
        tool = self.tools.get(tool_name)

        if not tool:
            return f"Tool '{tool_name}' not found"

        return tool(input_data)

    def run(self, task):
        self.remember(task)

        if any(char.isdigit() for char in task):
            result = self.use_tool("calculator", task)

            return {
                "agent": self.name,
                "task": task,
                "tool": "calculator",
                "result": result,
                "status": "completed",
            }

        thought = self.think(task)

        return {
            "agent": self.name,
            "task": task,
            "thought": thought,
            "status": "completed",
        }