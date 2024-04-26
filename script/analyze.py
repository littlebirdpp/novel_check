import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

def load_data(file_path):
    # CSVファイルを読み込み
    return pd.read_csv(file_path)

def extract_keywords(data):
    # キーワードをカウント
    keyword_counts = Counter()
    for keywords in data['keyword']:
        for keyword in keywords.split():
            keyword_counts[keyword] += 1
    return keyword_counts

def create_keyword_graph(keyword_counts):
    # キーワードの接続グラフを作成
    G = nx.Graph()
    for keyword, count in keyword_counts.items():
        G.add_node(keyword, size=count)
    # ここではすべてのキーワードを無差別に接続しています
    keywords = list(keyword_counts.keys())
    for i in range(len(keywords)):
        for j in range(i + 1, len(keywords)):
            G.add_edge(keywords[i], keywords[j])
    sizes = [G.nodes[node]['size']*10 for node in G]  # ノードのサイズを調整
    nx.draw(G, with_labels=True, node_size=sizes)
    plt.savefig('keyword_graph.png')

def main(file_path):
    data = load_data(file_path)
    keyword_counts = extract_keywords(data)
    # 集計結果をDataFrameとして保存
    df = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Count'])
    df.to_csv('keyword_counts.csv', index=False)
    create_keyword_graph(keyword_counts)

if __name__ == '__main__':
    main('/data/narou_data_20240426_004336.csv')
