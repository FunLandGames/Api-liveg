from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

HF_API_KEY = os.environ.get("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    result = query({"inputs": user_message})

    try:
        reply = result[0]["generated_text"]
    except:
        reply = "Sorry, I am thinking..."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
