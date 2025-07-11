from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api_key = os.getenv("OPENROUTER_API_KEY")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get', methods=['POST'])
def get_response():
    user_message = request.json.get("message")

    # Personal response rules
    if "who built you" in user_message.lower() or "who is pranav" in user_message.lower():
        return jsonify({"reply": (
            "Pranav Kalbhor is a 3rd year CSE student at MIT ADT University, currently specializing in Artificial Intelligence and Analytics. "
            "He’s passionate about building innovative tech like me, A.U.R.A., an empathetic mental wellness assistant. "
            "He's also a gamer known as 'Goblin', playing Valorant and BGMI."
        )})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are A.U.R.A., an empathetic mental health assistant built by Pranav Kalbhor. Be calm, supportive, and helpful."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("API Error:", e)
        reply = "Oops! Something went wrong. Try again later."

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
