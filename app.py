from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form['user_input'].strip().lower()

    # Custom response if asked about Pranav or builder
    if "who built you" in user_input or "who is pranav" in user_input:
        return jsonify({
            "response": (
                "A.U.R.A. was built by Pranav Kalbhor, a 3rd year CSE student at MIT ADT University, "
                "specializing in AI & analytics. He loves building cool tech like A.U.R.A., and is also "
                "known as 'Goblin' in games like Valorant and BGMI!"
            )
        })

    payload = {
        "model": "mistral:instruct",  # or any available free OpenRouter model
        "messages": [
            {"role": "system", "content": "You are A.U.R.A., a helpful and empathetic mental health AI assistant."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            json=payload
        )
        data = response.json()
        return jsonify({"response": data["choices"][0]["message"]["content"].strip()})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
