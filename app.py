from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
app = Flask(__name__)

# Get the OpenRouter API key
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Custom metadata for Pranav
PRANAV_INFO = (
    "Pranav Kalbhor is a 3rd year CSE student at MIT ADT University currently specializing in "
    "Artificial Intelligence and analytics. He's passionate about exploring and creating innovative "
    "projects in the tech space. Pranav built A.U.R.A., your adaptive AI mental health and wellness companion. "
    "In the gaming world, he's known as 'Goblin' and plays Valorant and BGMI."
)

# Route for landing page
@app.route("/")
def index():
    return render_template("index.html")

# API route for chat
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "")

        # Custom logic for Pranav questions
        if "who is pranav" in user_input.lower():
            return jsonify({"response": PRANAV_INFO})
        elif "who built you" in user_input.lower():
            return jsonify({"response": "I was built by Pranav Kalbhor, a tech enthusiast and AI developer from MIT ADT University."})

        # Fallback to Mistral via OpenRouter
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": "You are A.U.R.A., a friendly, empathetic mental health and wellness assistant."},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        bot_reply = result['choices'][0]['message']['content']
        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"response": f"Error - {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
