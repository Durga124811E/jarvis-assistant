from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

APP_NAME = "Ultron"

# Simple local knowledge base; replace with real logic later
HELP_TEXT = {
    "hello": "Hello. I am Ultron. I can help with trading research, job tracking, work planning, project debugging, and safe ethical hacking guidance.",
    "hi": "Hello. Tell me what you want to do.",
    "help": "I can help you with trading research, project planning, coding, debugging, job search, tracking earning platforms, and learning cybersecurity safely.",
    "status": "Ultron is online and ready.",
    "trade": "I can help track watchlists, market news, risk notes, and trade journal entries; I cannot place trades or promise guaranteed returns.",
    "jobs": "I can help search, track, and prioritize job applications and earning-platform opportunities.",
    "project": "I can help plan work, break projects into tasks, track progress, and organize deadlines.",
    "debug": "Share the error, stack trace, or code snippet and I will help identify the likely bug and fix.",
    "hacking": "I can help with ethical hacking learning, defensive security concepts, Kali Linux terminology, and safe lab practice, not unauthorized access.",
    "linux": "I can help with standard Linux commands, troubleshooting, server tasks, and shell scripting.",
    "default": "I am Ultron. I can assist with trading research, work planning, coding, debugging, job tracking, and cybersecurity learning. Ask me what you need."
}

# In-memory storage for demo behavior
trades = []
alerts = []
projects = []
applications = []


def build_reply(message: str) -> str:
    text = (message or "").strip().lower()
    if not text:
        return "Please tell me what you want to do."

    if "trade" in text or "trading" in text:
        return HELP_TEXT["trade"]
    if "job" in text or "earning" in text or "platform" in text:
        return HELP_TEXT["jobs"]
    if "project" in text or "work" in text or "plan" in text:
        return HELP_TEXT["project"]
    if "debug" in text or "error" in text or "code" in text:
        return HELP_TEXT["debug"]
    if "hack" in text or "cyber" in text or "kali" in text:
        return HELP_TEXT["hacking"]
    if "linux" in text:
        return HELP_TEXT["linux"]
    if "help" in text:
        return HELP_TEXT["help"]
    if "hello" in text or "hi" in text:
        return HELP_TEXT["hello"]
    if "status" in text:
        return HELP_TEXT["status"]

    for key, value in HELP_TEXT.items():
        if key in text:
            return value

    return HELP_TEXT["default"]


@app.route("/")
def index():
    return render_template("ultron.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")
    response = build_reply(message)
    return jsonify({"reply": response})


@app.route("/api/trade", methods=["POST"])
def add_trade():
    payload = request.get_json(silent=True) or {}
    symbol = payload.get("symbol", "") or "UNKNOWN"
    side = payload.get("side", "") or "LONG"
    entry = payload.get("entry", "") or "0"
    stop = payload.get("stop", "") or "0"
    target = payload.get("target", "") or "0"
    note = payload.get("note", "") or ""

    trades.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol.upper(),
        "side": side.upper(),
        "entry": entry,
        "stop": stop,
        "target": target,
        "note": note,
    })
    return jsonify({"status": "ok", "trades": trades[-5:]})


@app.route("/api/trade", methods=["GET"])
def get_trades():
    return jsonify({"trades": trades})


@app.route("/api/project", methods=["POST"])
def add_project():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title", "") or "Untitled task"
    due = payload.get("due", "") or ""
    status = payload.get("status", "") or "planned"

    projects.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "title": title,
        "due": due,
        "status": status,
    })
    return jsonify({"status": "ok", "projects": projects})


@app.route("/api/project", methods=["GET"])
def get_projects():
    return jsonify({"projects": projects})


@app.route("/api/application", methods=["POST"])
def add_application():
    payload = request.get_json(silent=True) or {}
    company = payload.get("company", "") or "Unknown"
    role = payload.get("role", "") or "Unknown role"
    status = payload.get("status", "") or "applied"

    applications.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "company": company,
        "role": role,
        "status": status,
    })
    return jsonify({"status": "ok", "applications": applications})


@app.route("/api/application", methods=["GET"]) 
def get_applications():
    return jsonify({"applications": applications})


@app.route("/api/alert", methods=["POST"]) 
def add_alert():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "") or "New alert"
    alerts.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text,
    })
    return jsonify({"status": "ok", "alerts": alerts})


@app.route("/api/alert", methods=["GET"]) 
def get_alerts():
    return jsonify({"alerts": alerts})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
