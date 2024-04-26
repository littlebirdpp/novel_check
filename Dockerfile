# Pythonの公式イメージをベースにする
FROM python:3.11

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# Poetryをインストール
RUN pip install poetry

# Poetryの設定を変更（仮想環境を作成しないようにする）
RUN poetry config virtualenvs.create false

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock* ./

# 依存関係をインストール
RUN poetry install --no-root

# 日本語フォントのインストール
RUN apt-get update && apt-get install -y fonts-noto-cjk

# アプリケーションのファイルをコンテナ内にコピー
COPY . .

# コンテナを実行したときに実行するコマンド
CMD ["python", "./script/data_make.py","./script/analyze.py"]
