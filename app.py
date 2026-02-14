from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    # memory add
    chat_history.append("User: " + user_message)

    response = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-large",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"inputs": "\n".join(chat_history)}
    )

    result = response.json()

    try:
        ai_reply = result[0]["generated_text"]
    except:
        ai_reply = str(result)

    chat_history.append("Bot: " + ai_reply)

    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
