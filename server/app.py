from flask import Flask, render_template, send_file, jsonify
import json
from pathlib import Path

app = Flask(__name__)

def load_release_info():
    with open("release/release_info.json") as f:
        return json.load(f)

@app.route("/")
def download_page():
    release_info = load_release_info()
    return render_template("download.html", **release_info)

@app.route("/download/latest")
def download_latest():
    release_info = load_release_info()
    dmg_path = Path(f"release/FastFlagManager-{release_info['version']}.dmg")
    return send_file(dmg_path, as_attachment=True)

@app.route("/api/update-check")
def check_update():
    return jsonify(load_release_info())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 