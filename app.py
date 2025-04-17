from flask import Flask, make_response
from flask_cors import CORS  # ← 追加
import update_fire_map
import os

app = Flask(__name__)
CORS(app)  # ← 追加

@app.route("/run-map-update", methods=["POST"])
def run_map_update():
    try:
        result = update_fire_map.main()
        response = make_response(result, 200)
        response.mimetype = "text/plain"
        return response
    except Exception as e:
        response = make_response(f"❌ 実行失敗: {str(e)}", 500)
        response.mimetype = "text/plain"
        return response
