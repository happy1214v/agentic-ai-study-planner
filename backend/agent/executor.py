class Executor:
    def __init__(self, max_retries=2):
        self.max_retries = max_retries

    def execute_step(self, step):
        if not step or not str(step).strip():
            raise ValueError("Invalid or empty step")

        return f"Executed: {step}"

    def execute(self, plan):
        results = []

        if not plan:
            return {
                "status": "failed",
                "message": "No plan provided",
                "results": [],
            }

        for step in plan:
            attempts = 0
            success = False
            result = None
            error = None

            while attempts <= self.max_retries:
                attempts += 1

                try:
                    result = self.execute_step(step)
                    success = True
                    break

                except Exception as e:
                    error = str(e)

            if success:
                results.append({
                    "step": step,
                    "status": "completed",
                    "result": result,
                    "attempts": attempts,
                })
            else:
                results.append({
                    "step": step,
                    "status": "failed",
                    "result": error,
                    "attempts": attempts,
                })

        failed_steps = [
            item
            for item in results
            if item["status"] == "failed"
        ]

        overall_status = (
            "failed"
            if failed_steps
            else "completed"
        )

        return {
            "status": overall_status,
            "results": results,
        }