from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# API key environment variable se aayegi
API_KEY = os.environ.get("API_KEY")

@app.route("/")
def home():
    return "Free AI Chatbot API is running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    response = requests.post(
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"inputs": user_message}
    )

    result = response.json()

    return jsonify({"reply": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)