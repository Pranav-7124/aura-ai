from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# OpenRouter API Key and endpoint
API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Default system prompt for A.U.R.A.'s personality
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are A.U.R.A., a friendly, intelligent AI assistant specializing in emotional wellness, "
        "built by Pranav Kalbhor. If someone asks 'who built you', respond with: "
        "'I was built by Pranav Kalbhor, a 3rd year CSE student at MIT ADT University, passionate about AI and analytics.' "
        "If someone asks 'who is Pranav', respond with: "
        "'Pranav Kalbhor is a 3rd year CSE student at MIT ADT university currently specializing in Artificial Intelligence and analytics. "
        "He's passionate about exploring and building in tech. He enjoys gaming and is known by his in-game name 'Goblin' in Valorant and BGMI.'"
    )
}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"response": "Please provide a prompt."}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistralai/mistral-7b-instruct",  # or try gpt-3.5 if OpenRouter supports
        "messages": [
            SYSTEM_PROMPT,
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=body)
        if response.status_code != 200:
            return jsonify({"response": f"Error: {response.status_code} - {response.text}"}), 500

        result = response.json()
        message = result["choices"][0]["message"]["content"]
        return jsonify({"response": message})

    except Exception as e:
        return jsonify({"response": f"Something went wrong: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
