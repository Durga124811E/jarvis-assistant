from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os, json

app = Flask(__name__)
APP_NAME = "Ultron Voice Pro"
DATA_PATH = os.path.join(os.path.dirname(__file__), 'ultron_data.json')


def load_data():
    if not os.path.exists(DATA_PATH):
        return {"trades": [], "projects": [], "applications": [], "alerts": [], "notes": []}
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"trades": [], "projects": [], "applications": [], "alerts": [], "notes": []}


def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def build_reply(message: str) -> str:
    text = (message or '').strip().lower()
    if not text:
        return 'Please tell me what you need.'

    if any(k in text for k in ['hello', 'hi', 'hey']):
        return 'Hello. I am Ultron Voice Pro. I can help with trading research, jobs, project planning, debugging, Linux help, and ethical cybersecurity learning.'
    if any(k in text for k in ['help', 'commands', 'what can you do']):
        return "I can help with trading, jobs, projects, debugging, Linux, notes, dashboards, and safe ethical cybersecurity learning. Try: 'trade', 'jobs', 'projects', 'debug', 'linux', 'status', or 'teach me ethical hacking'."
    if any(k in text for k in ['trade', 'trading', 'watchlist', 'risk']):
        return 'I can help you log trade entries, manage watchlists, store risk notes, and review your trade plan. Use the trading panel.'
    if any(k in text for k in ['job', 'apply', 'earning', 'resume', 'platform']):
        return 'I can help you organize jobs, track applications, and prioritize follow-ups. Use the job tracker in the dashboard.'
    if any(k in text for k in ['project', 'task', 'plan', 'deadline', 'work']):
        return 'I can help you plan tasks, monitor progress, and create deadlines. Use the project board.'
    if any(k in text for k in ['debug', 'error', 'code', 'bug', 'stack']):
        return 'Send the error message, stack trace, or code snippet and I will help isolate likely causes and suggest a fix path.'
    if any(k in text for k in ['linux', 'bash', 'terminal', 'command', 'shell']):
        return 'I can assist with Linux commands, bash scripts, service troubleshooting, file operations, and system checks. Tell me the task.'
    if any(k in text for k in ['hacking', 'cyber', 'security', 'kali', 'ethical hacking']):
        return 'I can assist with ethical cybersecurity learning, Kali Linux concepts, defensive security workflows, and safe lab practice. I do not support unauthorized access.'
    if any(k in text for k in ['status', 'summary', 'overview']):
        data = load_data()
        return (
            f"Current overview: {len(data['trades'])} trade entries, {len(data['projects'])} project tasks, "
            f"{len(data['applications'])} applications, {len(data['notes'])} notes, {len(data['alerts'])} alerts."
        )
    return 'I understand the request. I can help with trading research, project planning, job tracking, debugging, Linux support, and ethical cybersecurity learning. Ask me in a clear way.'


@app.route('/')
def index():
    return render_template('ultron_voice.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get('message', '')
    return jsonify({'reply': build_reply(message)})


@app.route('/api/trade', methods=['GET'])
def get_trades():
    return jsonify({'trades': load_data().get('trades', [])})


@app.route('/api/trade', methods=['POST'])
def add_trade():
    data = load_data()
    payload = request.get_json(silent=True) or {}
    item = {
        'time': now(),
        'symbol': (payload.get('symbol') or 'UNKNOWN').upper(),
        'side': (payload.get('side') or 'LONG').upper(),
        'entry': payload.get('entry') or '0',
        'stop': payload.get('stop') or '0',
        'target': payload.get('target') or '0',
        'note': payload.get('note') or '',
    }
    data['trades'].append(item)
    save_data(data)
    return jsonify({'status': 'ok', 'trades': data['trades']})


@app.route('/api/project', methods=['GET'])
def get_projects():
    return jsonify({'projects': load_data().get('projects', [])})


@app.route('/api/project', methods=['POST'])
def add_project():
    data = load_data()
    payload = request.get_json(silent=True) or {}
    item = {
        'time': now(),
        'title': payload.get('title') or 'Untitled task',
        'due': payload.get('due') or 'No due date',
        'status': payload.get('status') or 'planned',
    }
    data['projects'].append(item)
    save_data(data)
    return jsonify({'status': 'ok', 'projects': data['projects']})


@app.route('/api/application', methods=['GET'])
def get_applications():
    return jsonify({'applications': load_data().get('applications', [])})


@app.route('/api/application', methods=['POST'])
def add_application():
    data = load_data()
    payload = request.get_json(silent=True) or {}
    item = {
        'time': now(),
        'company': payload.get('company') or 'Unknown',
        'role': payload.get('role') or 'Unknown role',
        'status': payload.get('status') or 'applied',
    }
    data['applications'].append(item)
    save_data(data)
    return jsonify({'status': 'ok', 'applications': data['applications']})


@app.route('/api/alert', methods=['GET'])
def get_alerts():
    return jsonify({'alerts': load_data().get('alerts', [])})


@app.route('/api/alert', methods=['POST'])
def add_alert():
    data = load_data()
    payload = request.get_json(silent=True) or {}
    item = {'time': now(), 'text': payload.get('text') or 'New alert'}
    data['alerts'].append(item)
    save_data(data)
    return jsonify({'status': 'ok', 'alerts': data['alerts']})


@app.route('/api/notes', methods=['GET'])
def get_notes():
    return jsonify({'notes': load_data().get('notes', [])})


@app.route('/api/notes', methods=['POST'])
def add_note():
    data = load_data()
    payload = request.get_json(silent=True) or {}
    item = {'time': now(), 'text': payload.get('text') or 'No note'}
    data['notes'].append(item)
    save_data(data)
    return jsonify({'status': 'ok', 'notes': data['notes']})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
