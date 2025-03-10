from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel
import os
import subprocess
import json
import requests
import sqlite3
import shutil

app = FastAPI()

data_directory = "./data/"

LLM_API_BASE = "https://aiproxy.sanand.workers.dev/openai/v1"
LLM_API_KEY = os.environ.get("evyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDY0MzhAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.cVZQ9PdwcVpCw0uUIchzua3Skut2HmVioyiE47VkDkU")

def call_llm_api(prompt):
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 100
    }
    response = requests.post(f"{LLM_API_BASE}/completions", headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["text"].strip()

class TaskRequest(BaseModel):
    task: str

@app.post("/run")
def run_task(request: TaskRequest):
    task = request.task.lower()
    
    try:
        if "count wednesdays" in task:
            return count_wednesdays()
        elif "sort json contacts" in task:
            return sort_json_contacts()
        elif "install uv" in task and "run datagen.py" in task:
            return install_and_run_datagen(request.task)
        elif "format contents" in task and "prettier" in task:
            return format_contents()
        elif "write first line of the 10 most recent .log files" in task:
            return write_recent_logs()
        elif "find all markdown files" in task:
            return create_markdown_index()
        elif "extract sender's email address" in task:
            return extract_email_sender()
        elif "extract credit card number" in task:
            return extract_credit_card_number()
        elif "find the most similar pair of comments" in task:
            return find_similar_comments()
        elif "total sales of all the items in the 'Gold' ticket type" in task:
            return calculate_total_sales()
        elif "fetch data from an api" in task:
            return fetch_data_from_api()
        elif "clone a git repo" in task:
            return clone_git_repo()
        elif "run a sql query" in task:
            return run_sql_query()
        elif "scrape a website" in task:
            return scrape_website()
        elif "compress or resize an image" in task:
            return compress_or_resize_image()
        elif "transcribe audio from an mp3 file" in task:
            return transcribe_audio()
        elif "convert markdown to html" in task:
            return convert_markdown_to_html()
        elif "filter a csv file" in task:
            return filter_csv_file()
        else:
            raise HTTPException(status_code=400, detail="Invalid task description")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read", response_class=PlainTextResponse)
def read_file(path: str):
    full_path = os.path.join(data_directory, os.path.basename(path))
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(full_path, "r") as file:
        return file.read()

@app.get("/", response_class=HTMLResponse)
def get_form():
    html_content = """
    <!DOCTYPE html>
    <html>
    <body>

    <h2>POST Request to /run</h2>

    <form action="/submit" method="post">
      <label for="task">Task:</label><br><br>
      <input type="text" id="task" name="task" value="who is vicky kumar"><br><br>
      <input type="submit" value="Submit">
    </form> 

    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/submit")
def handle_form_submission(task: str = Form(...)):
    response = requests.post("http://127.0.0.1:8000/run", json={"task": task})
    return response.json()

def count_wednesdays():
    file_path = os.path.join(data_directory, "dates.txt")
    output_file = os.path.join(data_directory, "dates-wednesdays.txt")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="dates.txt not found")
    
    with open(file_path, "r") as f:
        dates = f.readlines()
    
    wednesdays = [date.strip() for date in dates if "Wednesday" in date]
    with open(output_file, "w") as f:
        f.write(str(len(wednesdays)))
    
    return {"message": "Wednesdays counted and saved", "file": output_file}

def sort_json_contacts():
    file_path = os.path.join(data_directory, "contacts.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="contacts.json not found")
    
    with open(file_path, "r") as f:
        contacts = json.load(f)
    
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    output_file = os.path.join(data_directory, "contacts-sorted.json")
    with open(output_file, "w") as f:
        json.dump(sorted_contacts, f, indent=4)
    
    return {"message": "Contacts sorted", "file": output_file}

def install_and_run_datagen(email):
    try:
        subprocess.run(["pip", "install", "uv"], check=True)
        subprocess.run(["python", "datagen.py", email], check=True)
        return {"message": "uv installed and datagen.py executed"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error running datagen.py: {str(e)}")

def format_contents():
    try:
        subprocess.run(["npx", "prettier@3.4.2", "--write", os.path.join(data_directory, "format.md")], check=True)
        return {"message": "Contents formatted"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error formatting contents: {str(e)}")

def write_recent_logs():
    try:
        log_files = sorted([f for f in os.listdir(os.path.join(data_directory, "logs")) if f.endswith(".log")], key=lambda x: os.path.getmtime(os.path.join(data_directory, "logs", x)), reverse=True)[:10]
        recent_logs = []
        for log_file in log_files:
            with open(os.path.join(data_directory, "logs", log_file), "r") as f:
                recent_logs.append(f.readline().strip())
        output_file = os.path.join(data_directory, "logs-recent.txt")
        with open(output_file, "w") as f:
            f.write("\n".join(recent_logs))
        return {"message": "Recent logs written", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing recent logs: {str(e)}")

def create_markdown_index():
    try:
        md_files = [f for f in os.listdir(os.path.join(data_directory, "docs")) if f.endswith(".md")]
        index = {}
        for md_file in md_files:
            with open(os.path.join(data_directory, "docs", md_file), "r") as f:
                for line in f:
                    if line.startswith("# "):
                        index[md_file] = line[2:].strip()
                        break
        output_file = os.path.join(data_directory, "docs", "index.json")
        with open(output_file, "w") as f:
            json.dump(index, f, indent=4)
        return {"message": "Markdown index created", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating markdown index: {str(e)}")

def extract_email_sender():
    try:
        with open(os.path.join(data_directory, "email.txt"), "r") as f:
            email_content = f.read()
        prompt = f"Extract the sender's email address from the following email content:\n\n{email_content}"
        sender_email = call_llm_api(prompt)
        output_file = os.path.join(data_directory, "email-sender.txt")
        with open(output_file, "w") as f:
            f.write(sender_email)
        return {"message": "Email sender extracted", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting email sender: {str(e)}")

def extract_credit_card_number():
    try:
        with open(os.path.join(data_directory, "credit-card.png"), "rb") as f:
            image_data = f.read()
        prompt = "Extract the credit card number from the following image data."
        card_number = call_llm_api(prompt)
        output_file = os.path.join(data_directory, "credit-card.txt")
        with open(output_file, "w") as f:
            f.write(card_number.replace(" ", ""))
        return {"message": "Credit card number extracted", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting credit card number: {str(e)}")

def find_similar_comments():
    try:
        with open(os.path.join(data_directory, "comments.txt"), "r") as f:
            comments = f.readlines()
        prompt = f"Find the most similar pair of comments from the following list:\n\n{comments}"
        similar_comments = call_llm_api(prompt)
        comment1, comment2 = similar_comments.split("\n")
        output_file = os.path.join(data_directory, "comments-similar.txt")
        with open(output_file, "w") as f:
            f.write(comment1 + "\n" + comment2)
        return {"message": "Similar comments found", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding similar comments: {str(e)}")

def calculate_total_sales():
    try:
        conn = sqlite3.connect(os.path.join(data_directory, "ticket-sales.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(price * units) FROM tickets WHERE type = 'Gold'")
        total_sales = cursor.fetchone()[0]
        conn.close()
        output_file = os.path.join(data_directory, "ticket-sales-gold.txt")
        with open(output_file, "w") as f:
            f.write(str(total_sales))
        return {"message": "Total sales calculated", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating total sales: {str(e)}")

def fetch_data_from_api():
    try:
        response = requests.get("https://api.example.com/data")
        response.raise_for_status()
        data = response.json()
        output_file = os.path.join(data_directory, "api-data.json")
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        return {"message": "Data fetched from API", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from API: {str(e)}")

def clone_git_repo():
    try:
        repo_url = "https://github.com/example/repo.git"
        repo_dir = os.path.join(data_directory, "repo")
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
        with open(os.path.join(repo_dir, "new_file.txt"), "w") as f:
            f.write("This is a new file.")
        subprocess.run(["git", "add", "new_file.txt"], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add new file"], cwd=repo_dir, check=True)
        return {"message": "Git repo cloned and committed"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error cloning git repo: {str(e)}")

def run_sql_query():
    try:
        conn = sqlite3.connect(os.path.join(data_directory, "database.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM table_name")
        rows = cursor.fetchall()
        conn.close()
        output_file = os.path.join(data_directory, "query-results.json")
        with open(output_file, "w") as f:
            json.dump(rows, f, indent=4)
        return {"message": "SQL query executed", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running SQL query: {str(e)}")

def scrape_website():
    try:
        response = requests.get("https://example.com")
        response.raise_for_status()
        html_content = response.text
        output_file = os.path.join(data_directory, "scraped-content.html")
        with open(output_file, "w") as f:
            f.write(html_content)
        return {"message": "Website scraped", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping website: {str(e)}")

def compress_or_resize_image():
    try:
        from PIL import Image
        input_file = os.path.join(data_directory, "image.png")
        output_file = os.path.join(data_directory, "image-compressed.png")
        with Image.open(input_file) as img:
            img = img.resize((img.width // 2, img.height // 2))
            img.save(output_file, "PNG", optimize=True)
        return {"message": "Image compressed or resized", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error compressing or resizing image: {str(e)}")

def transcribe_audio():
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        audio_file = os.path.join(data_directory, "audio.mp3")
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        output_file = os.path.join(data_directory, "transcription.txt")
        with open(output_file, "w") as f:
            f.write(text)
        return {"message": "Audio transcribed", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")

def convert_markdown_to_html():
    try:
        import markdown
        input_file = os.path.join(data_directory, "document.md")
        output_file = os.path.join(data_directory, "document.html")
        with open(input_file, "r") as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content)
        with open(output_file, "w") as f:
            f.write(html_content)
        return {"message": "Markdown converted to HTML", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting markdown to HTML: {str(e)}")

def filter_csv_file():
    try:
        import csv
        input_file = os.path.join(data_directory, "data.csv")
        output_file = os.path.join(data_directory, "filtered-data.json")
        filtered_data = []
        with open(input_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["column_name"] == "filter_value":
                    filtered_data.append(row)
        with open(output_file, "w") as f:
            json.dump(filtered_data, f, indent=4)
        return {"message": "CSV file filtered", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filtering CSV file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
