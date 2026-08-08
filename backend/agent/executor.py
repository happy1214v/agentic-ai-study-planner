class Executor:
    def execute(self, plan):
        results = []

        for step in plan:
            results.append({
                "step": step,
                "status": "completed"
            })

        return results