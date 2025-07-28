import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-8192"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

history_path = "chat_history.json"

def ask_bot(prompt, model=GROQ_MODEL):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    try:
        response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def generate_questions(domain, difficulty, num_questions):
    prompt = f"Generate {num_questions} unique {difficulty} interview questions from the domain '{domain}'. Only include the question and its answer in Q: ... A: ... format."
    result = ask_bot(prompt)
    questions = []
    for qa in result.split("Q: ")[1:]:
        parts = qa.strip().split("A:")
        if len(parts) == 2:
            questions.append({"question": parts[0].strip(), "answer": parts[1].strip()})
    return questions

def save_chat_history(username, history):
    try:
        with open(history_path, "r") as f:
            all_history = json.load(f)
    except FileNotFoundError:
        all_history = {}

    all_history[username] = history
    with open(history_path, "w") as f:
        json.dump(all_history, f, indent=4)

def load_chat_history(username):
    try:
        with open(history_path, "r") as f:
            all_history = json.load(f)
        return all_history.get(username, [])
    except FileNotFoundError:
        return []
