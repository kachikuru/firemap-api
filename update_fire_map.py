
import pandas as pd
from haversine import haversine, Unit
from utils import fetch_latest_fire_address, geocode_address, load_hydrant_data, extract_nearby_hydrants, save_to_csv

def main():
    # 最新の火災住所を取得
    fire_address = fetch_latest_fire_address()

    # 消火栓データ全体を読み込み
    all_hydrants = load_hydrant_data("hydrants.csv")

    if fire_address:
        print(f"火災住所が検出されました: {fire_address}")
        fire_location = geocode_address(fire_address)

        if fire_location:
            hydrants_near_fire = extract_nearby_hydrants(fire_location, all_hydrants, radius=200)
            print(f"火災現場付近の消火栓数: {len(hydrants_near_fire)}")
            save_to_csv(hydrants_near_fire, "hydrants_near_fire.csv")
        else:
            print("住所のジオコーディングに失敗しました。全体データを出力します。")
            save_to_csv(all_hydrants, "hydrants_near_fire.csv")
    else:
        print("火災は検出されませんでした。茅ヶ崎市全体の消火栓を出力します。")
        save_to_csv(all_hydrants, "hydrants_near_fire.csv")

if __name__ == "__main__":
    main()
