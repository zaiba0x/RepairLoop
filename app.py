import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from hindsight_client import Hindsight
from memory import save_memory, search_memory
load_dotenv()

app = Flask(__name__)

DATA_FILE = "repair_cases.json"
BANK_ID = "repair-loop"

API_KEY = os.getenv("HINDSIGHT_API_KEY")

client = None

if API_KEY:
    try:
        client = Hindsight(
            base_url="https://api.hindsight.vectorize.io",
            api_key=API_KEY
        )
    except Exception as e:
        print("Hindsight connection error:", e)


def load_cases():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_cases(cases):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(cases, file, indent=4)


@app.route("/")
def home():
    cases = load_cases()
    return render_template("index.html", cases=cases)


@app.route("/add", methods=["POST"])
def add_case():
    data = request.get_json(silent=True) or {}

    device = data.get("device", "").strip()
    problem = data.get("problem", "").strip()
    solution = data.get("solution", "").strip()
    outcome = data.get("outcome", "").strip()

    if not all([device, problem, solution, outcome]):
        return jsonify({"error": "Please fill in all fields."}), 400

    case = {
        "device": device,
        "problem": problem,
        "solution": solution,
        "outcome": outcome
    }

    cases = load_cases()
    cases.insert(0, case)
    save_cases(cases)

    memory_saved = False

    memory_saved = save_memory(
    device,
    problem,
    solution,
    outcome
)
    return jsonify({
        "message": "Repair case saved successfully!",
        "memory_saved": memory_saved,
        "case": case
    })


@app.route("/search", methods=["POST"])
def search_cases():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip().lower()

    if not query:
        return jsonify({"error": "Enter a problem to search."}), 400

    cases = load_cases()
    words = query.split()

    matches = []

    for case in cases:
        text = " ".join([
            case.get("device", ""),
            case.get("problem", ""),
            case.get("solution", ""),
            case.get("outcome", "")
        ]).lower()

        if all(word in text for word in words):
            matches.append(case)

    memory_results = search_memory(query)
    return jsonify({
        "matches": matches,
        "memory_results": memory_results,
        "message": (
            f"Found {len(matches)} matching repair case(s)."
            if matches
            else "No exact local matches found."
        )
    })
    if __name__ == "__main__":
        app.run(debug=True)