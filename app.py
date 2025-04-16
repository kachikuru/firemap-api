from flask import Flask
import update_fire_map  # あなたのマップ更新スクリプトを使う
import os  # ← ポート指定のために必要

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

# 🔧 Renderが必要とするポート指定
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Renderから渡されるPORTを使う
    app.run(host="0.0.0.0", port=port)

