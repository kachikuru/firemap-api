from flask import Flask
import update_fire_map  # あなたのマップ更新スクリプトを使う

app = Flask(__name__)

@app.route("/run-map-update", methods=["POST"])
def run_map_update():
    try:
        update_fire_map.main()  # これがマップ更新のメイン関数
        return "✅ マップ更新完了", 200
    except Exception as e:
        return f"❌ 実行失敗: {str(e)}", 500

@app.route("/")
def home():
    return "🚒 FireMap API is running!"
