from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='static')

# ======================
# ROUTE: HOME
# ======================
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


# ======================
# ROUTE: DECISION ENGINE
# ======================
@app.route('/decision', methods=['POST'])
def decision():
    data = request.get_json()
    user_input = data.get("input", "")

    # ===== KING DIadem CORE =====
    result = f"KING DIADEM PROCESSED: {user_input}"

    return jsonify({
        "status": "success",
        "result": result
    })


# ======================
# HEALTH CHECK (สำคัญมาก)
# ======================
@app.route('/health')
def health():
    return "OK", 200


# ======================
# RUN LOCAL ONLY
# ======================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
