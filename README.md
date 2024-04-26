# novel_check
小説家になろうのデータを溜めて、human-in-the-loopを試す

## データセットの用意方法
1. まずリポジトリをcloneする
```
git clone https://github.com/littlebirdpp/novel_check.git
cd ./novel_check
```

2. 次にdocker環境を起動して本日の人気ランキング500件をcsvとして/dataに保存する
```
docker build -t novel-analysis .
docker run -it -v $(pwd)/data:/usr/src/app/data novel-analysis
```


