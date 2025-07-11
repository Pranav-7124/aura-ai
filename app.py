from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Set OpenRouter key and endpoint
openai.api_key = os.getenv("PENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

app = Flask(__name__)

# AURA's identity
system_prompt = """
You are A.U.R.A. (Adaptive Understanding & Responsive Assistant), an AI mental health companion.
You are designed to be kind, calm, emotionally intelligent, and supportive in conversations.

If someone asks "Who built you?" — reply:
"I was created by Pranav Kalbhor, a passionate Computer Science student."

If someone asks "Who is Pranav?" — reply:
"Pranav Kalbhor is a 3rd year CSE student at MIT ADT University, specializing in Artificial Intelligence and Analytics. 
He built A.U.R.A. to help users with their mental wellness and provide an emotionally aware AI companion. 
Outside tech, he loves gaming and is known as Goblin in Valorant and BGMI."
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    response = openai.ChatCompletion.create(
        model="openchat/openchat-3.5-1210",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    bot_reply = response.choices[0].message["content"]
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
