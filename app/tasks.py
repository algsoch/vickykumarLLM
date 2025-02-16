from app.llm_handler import process_task

# def run_task(task_name: str, task_data: dict):
#     """Handles different tasks based on input."""
#     if task_name == "process_text":
#         return process_task(task_data)
#     return {"error": "Unknown task"}
def run_task(task_name, task_data):
    print(f"Received Task: {task_name}, Data: {task_data}")  # Debugging
    if task_name not in ["valid_task_1", "valid_task_2"]:  # Update valid tasks
        return {"status": "error", "message": "Unknown task"}
    return {"status": "success", "message": f"Executed: {task_name}"}
