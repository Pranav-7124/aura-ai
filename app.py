from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://aura-ai.onrender.com",  # change if needed
    "X-Title": "AURA",
}

def custom_logic(user_input):
    lower_input = user_input.lower()
    if "who built you" in lower_input or "who is your creator" in lower_input or "who made you" in lower_input:
        return (
            "I was built by **Pranav Kalbhor**, a 3rd year CSE student at MIT ADT University, "
            "specializing in AI and analytics. He's passionate about tech innovation and loves creating new things. "
            "In his free time, he games under the name **Goblin** in Valorant and BGMI!"
        )
    elif "who is pranav" in lower_input:
        return (
            "**Pranav Kalbhor** is a tech enthusiast and builder from MIT ADT University. "
            "He specializes in Artificial Intelligence and Analytics. Also known as **Goblin**, "
            "he enjoys competitive gaming and building cool AI tools like me — A.U.R.A.!"
        )
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    special_response = custom_logic(user_input)
    if special_response:
        return jsonify({"response": special_response})

    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are A.U.R.A., an emotionally supportive and smart AI assistant."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Error connecting to A.U.R.A: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
