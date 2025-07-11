from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('message')

    # Custom response to "who is pranav"
    if "who is pranav" in user_input.lower():
        response_text = (
            "Pranav Kalbhor is a 3rd year CSE student at MIT ADT University, specializing in AI & Analytics. "
            "He's passionate about tech, gaming, and innovation. He built A.U.R.A., your adaptive mental wellness companion. "
            "He also goes by 'Goblin' in games like Valorant and BGMI."
        )
    elif "who built you" in user_input.lower():
        response_text = "I was built by Pranav Kalbhor – a brilliant AI enthusiast from MIT ADT University."
    else:
        try:
            response = client.chat.completions.create(
                model="openchat/openchat-3.5-1210",
                messages=[
                    {"role": "system", "content": "You are A.U.R.A., a friendly, Gen Z mental health AI companion."},
                    {"role": "user", "content": user_input}
                ]
            )
            response_text = response.choices[0].message.content
        except Exception as e:
            response_text = f"A.U.R.A.: Error - {str(e)}"

    return jsonify({'reply': response_text})
