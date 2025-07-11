from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')

    # Special response override
    if "who built you" in user_input.lower():
        return jsonify({
            "reply": "I was built by Pranav Kalbhor, a 3rd year CSE student at MIT ADT University, specializing in Artificial Intelligence and analytics. He's passionate about creating tech wonders. In the gaming world, he's known as 'Goblin' and loves playing Valorant and BGMI."
        })
    if "who is pranav" in user_input.lower():
        return jsonify({
            "reply": "Pranav Kalbhor is a talented tech enthusiast and a 3rd year CSE student at MIT ADT University. He specializes in AI & analytics and enjoys building intelligent tools like me—A.U.R.A. He's also a passionate gamer known as 'Goblin'."
        })

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://aura-ai.onrender.com",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "system", "content": "You are A.U.R.A., a warm, friendly AI mental wellness assistant. Be supportive, engaging, and helpful. Add occasional emojis and Gen Z-friendly tone."},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()

        if "choices" in result:
            reply = result['choices'][0]['message']['content']
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": f"Error: {result}"})

    except Exception as e:
        return jsonify({"reply": f"Error connecting to A.U.R.A: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True)
