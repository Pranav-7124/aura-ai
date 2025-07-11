import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Set up OpenRouter client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json['prompt']

        # Special custom response if asked about Pranav
        if "who built you" in user_input.lower() or "who is pranav" in user_input.lower():
            return jsonify({
                'response': (
                    "I was built by Pranav Kalbhor — a 3rd year CSE student at MIT ADT University, "
                    "specializing in Artificial Intelligence and Analytics. He's passionate about creating tech experiences "
                    "like A.U.R.A. and is also known as 'Goblin' in Valorant and BGMI."
                )
            })

        # Generate reply from OpenRouter
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are A.U.R.A., a friendly and thoughtful mental health AI assistant created by Pranav Kalbhor."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({'response': reply})

    except Exception as e:
        return jsonify({'response': f"Error connecting to A.U.R.A: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
