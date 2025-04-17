import requests
from bs4 import BeautifulSoup
import pandas as pd
from haversine import haversine, Unit
from ftplib import FTP
from time import sleep

# 🔑 Google Maps APIキー（ご自身のものに変更）
GOOGLE_API_KEY = "AIzaSyAkkka4OrpBbxztgEizSYQ1lPhtSjBadN0"

# 🔧 FTP設定（エックスサーバーの情報に合わせて設定）
FTP_HOST = "sv14277.xserver.jp"
FTP_USER = "kasai@kachikuru.net"
FTP_PASS = "chigasaki202"
LOCAL_FILE = "hydrants_near_fire.csv"

def get_latest_fire_address():
    url = "http://www.chigasaki-samukawa119.info/chigasaki-saigai/index.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table")
    if not table:
        print("❌ テーブルが見つかりません")
        return None

    rows = table.find_all("tr")[1:]  # ヘッダーを除外
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 3:
            fire_type = cells[1].text.strip()
            address = cells[2].text.strip()
            if "火災" in fire_type:
                message = f"{address}で{fire_type}が発生しました。"
                print(f"🔥 最新の火災情報: {message}")
                return message

    print("ℹ️ 現在、火災情報は見つかりませんでした")
    return None

def get_coordinates(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]
        print(f"📍 座標: 緯度 {lat}, 経度 {lng}")
        return lat, lng
    else:
        print(f"❌ 緯度経度の取得失敗：{data['status']}")
        return None, None

def filter_hydrants(fire_lat, fire_lng):
    df = pd.read_csv("hydrants.csv")
    lat_col = "経度"
    lng_col = "緯度"

    df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
    df[lng_col] = pd.to_numeric(df[lng_col], errors='coerce')
    df = df.dropna(subset=[lat_col, lng_col])

    fire_point = (fire_lat, fire_lng)

    def within_range(row):
        point = (row[lat_col], row[lng_col])
        return haversine(fire_point, point, unit=Unit.METERS) <= 200

    nearby = df[df.apply(within_range, axis=1)]
    nearby.to_csv(LOCAL_FILE, index=False, encoding="utf-8-sig")
    print(f"✅ 抽出完了！{len(nearby)}件の消火栓・防火水槽が見つかりました。")

def upload_csv_via_ftp():
    try:
        with FTP(FTP_HOST) as ftp:
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            print("🔗 FTPログイン成功")
            ftp.cwd("/public_html/wp-content/uploads/2025/04")
            print(f"📁 アップロード先: {ftp.pwd()}")
            with open(LOCAL_FILE, "rb") as f:
                ftp.storbinary("STOR hydrants_near_fire.csv", f)
            print("✅ WordPressにCSVを自動アップロードしました！")
    except Exception as e:
        print("❌ FTPアップロード失敗:", e)

def main():
    fire_message = get_latest_fire_address()
    if not fire_message:
        return "現在、火災発生の情報はありません。"

    address = fire_message.split("で")[0].strip()
    sleep(1)
    lat, lng = get_coordinates(address)
    if lat and lng:
        filter_hydrants(lat, lng)
        upload_csv_via_ftp()
        return fire_message
    else:
        return "❌ 緯度経度の取得に失敗しました"

if __name__ == "__main__":
    print(main())

