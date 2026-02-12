import requests
from flask import Flask, request, jsonify, render_template
from services.calculator import calculate_construction
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- CALCULATOR ----------------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    def safe_float(val):
        try:
            return float(val)
        except:
            return 0

    area = safe_float(data.get("area"))
    floors = data.get("floors", "G+1")
    wage = safe_float(data.get("wage"))
    cost = safe_float(data.get("cost"))

    result = calculate_construction(area, floors, wage, cost)

    return jsonify(result)

#---------------- CHATBOT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()

    # Simple intelligent responses
    if "hello" in user_message or "hi" in user_message:
        ai_reply = "Hello! I am your BuildWise AI assistant. I can explain your construction plan."

    elif "cost" in user_message:
        ai_reply = "The total cost is calculated using labor and material expenses based on your area and floors."

    elif "workers" in user_message:
        ai_reply = "Workers are assigned based on total construction area and divided into roles like masons, helpers, electricians, and supervisors."

    elif "schedule" in user_message:
        ai_reply = "The project is divided into weekly phases like foundation, structure, finishing, and inspection."

    elif "sustainability" in user_message:
        ai_reply = "We suggest eco-friendly materials like fly-ash bricks and solar roofing to reduce carbon impact."

    elif "plan" in user_message:
        ai_reply = "You can choose between fast-track, balanced, budget, or high-quality construction plans."

    else:
        ai_reply = "I can help explain cost, workers, schedule, sustainability, or construction plans."

    return jsonify({"reply": ai_reply})



if __name__ == "__main__":
    app.run(debug=True)
