from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)

# A.U.R.A.'s memory and personality
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

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    bot_reply = response.choices[0].message.content
    return jsonify({"reply": bot_reply})

# Run the app locally (ignored on Render)
if __name__ == "__main__":
    app.run(debug=True)
