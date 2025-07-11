from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Initialize OpenRouter or OpenAI API (Use proper API key from .env)
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))
model = "openrouter/mistralai/mistral-7b-instruct"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    # Handle custom bot logic
    lower_msg = user_message.lower()
    if "who built you" in lower_msg or "who is your creator" in lower_msg:
        return jsonify({
            "response": "I was built by Pranav Kalbhor, a 3rd year CSE student at MIT ADT University, passionate about AI and innovation. He created A.U.R.A. to help others with mental wellness and support. You might also know him by his in-game name 'Goblin' in Valorant and BGMI. 🎮"
        })
    elif "who is pranav" in lower_msg:
        return jsonify({
            "response": "Pranav Kalbhor is a 3rd year Computer Science student at MIT ADT University, specializing in AI and analytics. He's passionate about tech innovation and mental health support. He's also a gamer known as 'Goblin'."
        })

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are A.U.R.A., an AI mental health and emotional support companion. Be kind, caring, and empathetic."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Error connecting to A.U.R.A: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
