import pandas as pd
import requests
import matplotlib as mpl
mpl.rcParams['font.family'] ='Noto Sans CJK JP'
import matplotlib.pyplot as plt
import japanize_matplotlib  
import networkx as nx
import scipy
from itertools import combinations
from collections import Counter
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
                genre = novel['genre']
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
    return df

def filter_keywords(keyword_counts, min_count=2):
    # 出現回数がmin_countより大きいキーワードのみを保持
    return {k: v for k, v in keyword_counts.items() if v >= min_count}

def extract_keywords(data):
    # キーワードをカウント
    keyword_counts = Counter()
    for keywords in data['keyword']:
        for keyword in keywords.split():
            keyword_counts[keyword] += 1
    return keyword_counts

def create_keyword_graph(df,timestamp):
    # NaNを空文字で置き換える
	df['keyword'] = df['keyword'].fillna('')

	# キーワードを個別のトークンに分割
	keywords = df['keyword'].apply(lambda x: x.split())

	# 共起するキーワードのペアをカウント
	keyword_pairs = Counter()
	for keyword_list in keywords:
		for pair in combinations(set(keyword_list), 2):
			sorted_pair = tuple(sorted(pair))
			keyword_pairs[sorted_pair] += 1

	# ネットワークグラフを作成
	G = nx.Graph()

	# キーワードペアとその出現頻度をエッジとして追加
	for pair, weight in keyword_pairs.items():
		G.add_edge(pair[0], pair[1], weight=weight)

	# グラフを描画
	plt.figure(figsize=(40, 40)) # グラフのサイズを20インチx20インチに設定
	pos = nx.spring_layout(G, seed=42)  # ノードの位置
	nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
	nx.draw_networkx_edges(G, pos, width=1)
	nx.draw_networkx_labels(G, pos, font_size=10, font_family='Noto Sans CJK JP')
	plt.savefig(f'data/keyword_graph_{timestamp}.png')
        
	# 全ての頂点について探索
	all_friends_of_friends = []

	for vertex in G.nodes():
		# 最短経路1で到達できるノード（直接の友達）
		friends_level_1 = set(G[vertex])

		# 最短経路2で到達できるノード（友達の友達）
		friends_level_2 = set()
		for friend in friends_level_1:
			friends_level_2.update(G[friend])

		# 頂点自身を含める（比較のため）
		friends_level_2.add(vertex)

		# 直接つながっていないノードのみを抽出
		final_set = set()
		for fof in friends_level_2:
			if fof not in G[vertex] and fof != vertex:
				final_set.add(fof)

		# リストに追加
		for fof in final_set:
			all_friends_of_friends.append({
				'Vertex': vertex,
				'Friend_of_Friend': fof
			})

	# DataFrameに変換
	df_friends_of_friends = pd.DataFrame(all_friends_of_friends)

	# CSVファイルとして保存
	df_friends_of_friends.to_csv(f'data/outputfile_{timestamp}..csv', index=False)
	return df_friends_of_friends



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
	df=save_data(data, filename)
	# keyword_counts = extract_keywords(data)
	# keyword_counts = filter_keywords(keyword_counts)
	# # 集計結果をDataFrameとして保存
	# df_key = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Count'])
	# df_key = df_key.sort_values('Count', ascending=False)  # カウントで降順にソート
	# df_key.to_csv(f'data/keyword_counts_{timestamp}.csv', index=False)
	# if not df.empty:
	# 	df_friends=create_keyword_graph(df,timestamp)
	# 	# df_keyから上位5位のキーワードを抽出
	# 	top_keywords = df_key['Keyword'].head(5)

	# 	# df_friendsから、そのキーワードにマッチするvertexの行のみをフィルタリング
	# 	df_filtered_friends = df_friends[df_friends['Vertex'].isin(top_keywords)]

	# 	# 結果をCSVファイルとして保存
	# 	df_filtered_friends.to_csv(f'data/filtered_friends_{timestamp}.csv', index=False)

	# 	print("Filtered friends CSV file has been saved.")

if __name__ == "__main__":
    main()