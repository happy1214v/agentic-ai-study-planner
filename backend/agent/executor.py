class Executor:

    def execute(self, plan):
        results = []

        if not plan:
            return {
                "status": "failed",
                "message": "No plan provided",
                "results": [],
            }

        for step in plan:
            if not step or not str(step).strip():
                results.append({
                    "step": step,
                    "status": "failed",
                    "result": "Invalid or empty step",
                })
                continue

            results.append({
                "step": step,
                "status": "completed",
                "result": f"Executed: {step}",
            })

        failed_steps = [
            item for item in results
            if item["status"] == "failed"
        ]

        if failed_steps:
            overall_status = "failed"
        else:
            overall_status = "completed"

        return {
            "status": overall_status,
            "results": results,
        }