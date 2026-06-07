import os
import sys

# Add parent directory to path so we can import agent/tools/memory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="../static", template_folder="../templates")
CORS(app)

# In-memory session store (per Vercel instance)
_agents = {}

def get_agent(session_id: str):
    if session_id not in _agents:
        from agent.assistant_agent import AssistantAgent
        _agents[session_id] = AssistantAgent()
    return _agents[session_id]


@app.route("/")
def index():
    return send_from_directory("../templates", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        return jsonify({"error": "GROQ_API_KEY not configured on the server."}), 500

    try:
        agent = get_agent(session_id)
        response = agent.chat(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def clear():
    data = request.get_json()
    session_id = data.get("session_id", "default")
    if session_id in _agents:
        _agents[session_id].memory_manager.clear_memory()
        del _agents[session_id]
    return jsonify({"status": "cleared"})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "groq_configured": bool(os.getenv("GROQ_API_KEY"))
    })


# Vercel needs this
if __name__ == "__main__":
    app.run(debug=True)
