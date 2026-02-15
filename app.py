from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# 🔑 GROQ API key from Replit secrets
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # Special response for creator question
    if "who created you" in user_message or "tumhe kisne banaya" in user_message:
        reply = "I was created by Lakshya 😎"
    else:
        try:
            response = client.chat.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_message}]
            )
            reply = response.choices[0].message["content"]
        except Exception as e:
            reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    user_feedback = data.get("feedback")
    print("Feedback received:", user_feedback)
    return jsonify({"status":"success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
