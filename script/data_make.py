import pandas as pd
import requests
import json
from datetime import datetime

def fetch_data(url,params):
    """ APIからデータを取得する関数 """
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data[0]['allcount'] > 0:
            # DataFrameを作成するための空のリストを準備
            ranking_data = []
            for i, novel in enumerate(data[1:], 1):
                title = novel['title']
                synopsis = novel['story']
                key = novel['keyword']
                biggenre =  novel['biggenre']
                genre = novel['biggenre']
                # ランキング、タイトル、あらすじをリストに追加
                ranking_data.append([i, title, synopsis, key, biggenre, genre])
            # リストをDataFrameに変換
            df = pd.DataFrame(ranking_data, columns=['Rank', 'Title', 'Synopsis', 'keyword', 'biggenre', 'genre'])
            return df
        else:
            print("No novels found.")
            return None
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def save_data(data, filename):
    """ 取得したデータをCSVファイルに保存する関数 """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    url = 'https://api.syosetu.com/novelapi/api/'
    params = {
        'out': 'json',
        'order': 'monthlypoint',  # 評価順に並べる
        'lim': 500,  # 上位10作品を取得
    }
    
    # データを取得
    data = fetch_data(url,params)
    
    # 現在の日時をファイル名に使用
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/narou_data_{timestamp}.csv"

    
    # データを保存
    save_data(data, filename)

if __name__ == "__main__":
    main()