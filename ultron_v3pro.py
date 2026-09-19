from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json, os

app = Flask(__name__)
APP_NAME = "Ultron v3 Pro"
DATA_FILE = os.path.join(os.path.dirname(__file__), "ultron_v3pro_data.json")


def default_data():
    return {
        "trades": [],
        "projects": [],
        "applications": [],
        "notes": [],
        "alerts": [],
    }


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(default_data())
        return default_data()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return default_data()
        for key in default_data().keys():
            data.setdefault(key, [])
        return data
    except Exception:
        return default_data()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def now_iso():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def build_reply(message: str) -> str:
    text = (message or "").strip().lower()
    if not text:
        return "Please tell me what you need."

    # Command routing
    if any(token in text for token in ["hello", "hi", "hey", "good morning", "good evening"]):
        return "Hello. I am Ultron v3 Pro. I can help with trading research, job tracking, project planning, debugging, Linux tasks, and ethical cybersecurity learning."

    if any(token in text for token in ["help", "commands", "what can you do"]):
        return "I can help with trading research, job tracking, task planning, note taking, Linux support, debugging, and ethical cybersecurity learning. Try: 'trade', 'jobs', 'projects', 'debug', 'linux', 'status', or 'hacking'."

    if any(token in text for token in ["trade", "trading", "watchlist", "risk", "journal"]):
        return "I can help you record trades, track stop and target levels, and maintain a disciplined risk journal. Use the trade panel to add entries."

    if any(token in text for token in ["job", "jobs", "application", "apply", "resume", "earning"]):
        return "I can help you track job opportunities, companies, application stages, and follow-up tasks. Use the application panel to update your pipeline."

    if any(token in text for token in ["project", "task", "plan", "schedule", "deadline", "work"]):
        return "I can help you organize tasks, deadlines, and priorities. Use the project board to add and track tasks."

    if any(token in text for token in ["debug", "error", "code", "bug", "stack"]):
        return "Send the stack trace, error output, or code snippet and I will help narrow the likely cause and suggest a fix strategy."

    if any(token in text for token in ["linux", "terminal", "bash", "shell", "server"]):
        return "I can help with basic Linux troubleshooting, shell commands, file operations, service checks, and scripting tasks. Tell me the exact goal or error."

    if any(token in text for token in ["hack", "hacking", "cyber", "security", "kali", "ethical"]):
        return "I can help with ethical cybersecurity learning, defensive security concepts, Kali Linux fundamentals, secure coding awareness, and safe lab practice. I do not support unauthorized access or illegal hacking."

    if any(token in text for token in ["status", "summary", "overview"]):
        data = load_data()
        return (
            f"Status overview: {len(data['trades'])} trade entries, {len(data['projects'])} project tasks, "
            f"{len(data['applications'])} applications, {len(data['notes'])} notes, and {len(data['alerts'])} alerts tracked."
        )

    return "I understand. I can help with trading, work planning, job tracking, debugging, Linux support, and ethical cybersecurity learning. Ask clearly and I will guide you."


@app.route("/")
def index():
    return render_template("ultron_v3pro.html")


@app.route("/api/chat", methods=["POST"]) 
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")
    return jsonify({"reply": build_reply(message)})


@app.route("/api/trade", methods=["GET"]) 
def get_trades():
    return jsonify({"trades": load_data().get("trades", [])})


@app.route("/api/trade", methods=["POST"]) 
def add_trade():
    data = load_data()
    payload = request.get_json(silent=True) or {}
    entry = {
        "time": now_iso(),
        "symbol": (payload.get("symbol") or "UNKNOWN").upper(),
        "side": (payload.get("side") or "LONG").upper(),
        "entry": payload.get("entry") or "0",
        "stop": payload.get("stop") or "0",
        "target": payload.get("target") or "0",
        "note": payload.get("note") or "",
    }
    data["trades"].append(entry)
    save_data(data)
    return jsonify({"status": "ok", "trades": data["trades"]})


@app.route("/api/project", methods=["GET"]) 
def get_projects():
    return jsonify({"projects": load_data().get("projects", [])})


@app.route("/api/project", methods=["POST"]) 
def add_project():
    data = load_data()
    payload = request.get_json(silent=True) or {}
    item = {
        "time": now_iso(),
        "title": payload.get("title") or "Untitled task",
        "due": payload.get("due") or "No due date",
        "status": payload.get("status") or "planned",
    }
    data["projects"].append(item)
    save_data(data)
    return jsonify({"status": "ok", "projects": data["projects"]})


@app.route("/api/application", methods=["GET"]) 
def get_applications():
    return jsonify({"applications": load_data().get("applications", [])})


@app.route("/api/application", methods=["POST"]) 
def add_application():
    data = load_data()
    payload = request.get_json(silent=True) or {}
    item = {
        "time": now_iso(),
        "company": payload.get("company") or "Unknown",
        "role": payload.get("role") or "Unknown role",
        "status": payload.get("status") or "applied",
    }
    data["applications"].append(item)
    save_data(data)
    return jsonify({"status": "ok", "applications": data["applications"]})


@app.route("/api/notes", methods=["GET"]) 
def get_notes():
    return jsonify({"notes": load_data().get("notes", [])})


@app.route("/api/notes", methods=["POST"]) 
def add_note():
    data = load_data()
    payload = request.get_json(silent=True) or {}
    item = {
        "time": now_iso(),
        "text": payload.get("text") or "No note text provided",
    }
    data["notes"].append(item)
    save_data(data)
    return jsonify({"status": "ok", "notes": data["notes"]})


@app.route("/api/alert", methods=["GET"]) 
def get_alerts():
    return jsonify({"alerts": load_data().get("alerts", [])})


@app.route("/api/alert", methods=["POST"]) 
def add_alert():
    data = load_data()
    payload = request.get_json(silent=True) or {}
    item = {
        "time": now_iso(),
        "text": payload.get("text") or "New alert",
    }
    data["alerts"].append(item)
    save_data(data)
    return jsonify({"status": "ok", "alerts": data["alerts"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
