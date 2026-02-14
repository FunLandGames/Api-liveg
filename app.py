import os
from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

# 🔑 Groq API key environment variable se lo
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "Please type a message!"})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Groq ka supported model
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
