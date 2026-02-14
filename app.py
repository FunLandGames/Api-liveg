# app.py
from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# 🔑 API key from Replit secrets
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "Please type something!"})

    try:
        response = client.chat.create(
            model="gpt-4o-mini",  # recommended free/active model
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
