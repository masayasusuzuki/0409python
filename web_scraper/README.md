# Webスクレイピングアプリ

このアプリケーションは、指定されたURLのウェブページを読み込み、テキスト情報を抽出するシンプルなWebスクレイパーです。Pythonと、FlaskとBeautifulSoup4を使用しています。

## 機能

- URLを入力して、ウェブページのテキスト情報を抽出
- CSSセレクタによる特定要素の抽出オプション
- レスポンシブなUI
- エラーハンドリング

## 必要なもの

- Python 3.6以降
- pip（Pythonパッケージマネージャー）

## インストール方法

1. リポジトリをクローンまたはダウンロードします
2. プロジェクトのルートディレクトリで以下のコマンドを実行して、必要なパッケージをインストールします：

```
pip install -r requirements.txt
```

## 使い方

1. プロジェクトのルートディレクトリで以下のコマンドを実行してアプリを起動します：

```
python app.py
```

2. ブラウザで `http://127.0.0.1:5000/` にアクセスします
3. フォームにURLを入力し、必要に応じてCSSセレクタを指定します
4. 「スクレイピング実行」ボタンをクリックして結果を確認します

## CSSセレクタの例

- `div.content` - class="content"を持つすべてのdiv要素
- `h1` - すべてのh1見出し
- `p.description` - class="description"を持つすべてのp要素
- `article > p` - article要素の直接の子である全てのp要素

## 注意事項

- 一部のWebサイトではスクレイピングが利用規約に違反する場合があります
- 公開されているAPIがある場合は、可能であればそちらを利用することを検討してください
- 過度なリクエストを送信して、対象のサーバに負荷をかけないようにしてください

## ライセンス

MIT

## 謝辞

- [Flask](https://flask.palletsprojects.com/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://requests.readthedocs.io/) 