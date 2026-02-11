from flask import Flask, request, jsonify, render_template
from services.calculator import calculate_construction

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    area = float(data.get("area", 0))
    floors = data.get("floors", "G+1")
    wage = float(data.get("wage", 0))
    cost = float(data.get("cost", 0))

    result = calculate_construction(area, floors, wage, cost)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
