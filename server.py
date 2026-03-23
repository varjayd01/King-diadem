import os
from flask import send_from_directory

from app import app

# ===== Serve index.html ข้างนอก =====
@app.route('/home')
def root_index():
    return send_from_directory('.', 'index.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
