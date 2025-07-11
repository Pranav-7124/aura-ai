from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

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
    user_input = request.json.get("message", "")

    # Custom response for questions about Pranav
    if "who built you" in user_input.lower() or "who is your creator" in user_input.lower():
        return jsonify({
            "response": "I was built by **Pranav Kalbhor**, a 3rd year CSE student at MIT ADT University, specializing in AI and analytics. He's passionate about tech, innovation, and mental health. He's also a gamer known as *Goblin* in BGMI and Valorant!"
        })
    elif "who is pranav" in user_input.lower():
        return jsonify({
            "response": "**Pranav Kalbhor** is a 3rd year CSE student at MIT ADT University. He specializes in AI and analytics and is passionate about building innovative tech solutions like me – A.U.R.A. He's also a gamer who goes by the name *Goblin* in Valorant and BGMI!"
        })

    payload = {
        "model": "openchat:free",
        "messages": [
            {
                "role": "system",
                "content": "You are A.U.R.A., a warm, friendly, and emotionally intelligent AI mental health assistant. Be helpful and supportive."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=HEADERS,
            json=payload
        )
        data = response.json()
        print("DEBUG RESPONSE:", data)

        # Check if choices exist
        if "choices" not in data:
            return jsonify({"response": "Oops! Something went wrong with A.U.R.A.'s response. Please try again shortly."})

        return jsonify({"response": data["choices"][0]["message"]["content"].strip()})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
