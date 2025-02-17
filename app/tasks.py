import os
import json
import subprocess
from app.llm_handler import extract_email_with_llm, extract_credit_card_with_llm

def execute_task(task: str):
    """
    Parses the given task and executes the appropriate function.
    """
    if "run external script" in task:
        return run_python_script("datagen.py")
    elif "format markdown" in task:
        return format_markdown("README.md")
    elif "count wednesdays" in task:
        return count_wednesdays()
    elif "sort contacts" in task:
        return sort_contacts()
    elif "extract email" in task:
        return extract_email_with_llm()
    elif "extract credit card" in task:
        return extract_credit_card_with_llm()
    else:
        raise ValueError("Unknown task")

def run_python_script(script_name: str):
    """Runs an external Python script securely."""
    script_path = os.path.join(os.getcwd(), script_name)
    if not os.path.exists(script_path):
        raise ValueError("Script not found")
    
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"

def format_markdown(file_path: str):
    """Formats a markdown file using Prettier."""
    result = subprocess.run(["npx", "prettier", "--write", file_path], capture_output=True, text=True)
    return "Markdown formatted successfully" if result.returncode == 0 else f"Error: {result.stderr}"

def count_wednesdays():
    """Counts the number of Wednesdays in /data/dates.txt"""
    file_path = os.path.join("data", "dates.txt")
    if not os.path.exists(file_path):
        raise FileNotFoundError("dates.txt not found")

    with open(file_path, "r") as file:
        lines = file.readlines()
    
  
