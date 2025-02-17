import os

def read_file_securely(path: str):
    """Securely reads a file from /data directory."""
    file_path = os.path.join("data", path)
    
    if ".." in path or path.startswith("/"):
        raise ValueError("Invalid file path")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
