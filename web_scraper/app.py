from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    scraped_data = None
    error = None
    url = ""
    
    if request.method == 'POST':
        url = request.form.get('url')
        selector = request.form.get('selector', '')
        
        if not url:
            error = "URLを入力してください"
        else:
            try:
                # URLからHTMLを取得
                response = requests.get(url)
                response.raise_for_status()  # ステータスコードが200番台でない場合例外を発生
                
                # BeautifulSoupでHTMLをパース
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # セレクタが指定されている場合は、そのセレクタに一致する要素を取得
                if selector:
                    elements = soup.select(selector)
                    if elements:
                        scraped_data = [element.get_text(strip=True) for element in elements]
                    else:
                        scraped_data = ["セレクタに一致する要素が見つかりませんでした"]
                else:
                    # セレクタが指定されていない場合は、全てのテキストを取得
                    # スクリプトとスタイルタグを除去
                    for script in soup(["script", "style"]):
                        script.extract()
                    
                    # テキストを取得
                    text = soup.get_text()
                    
                    # 改行と余分な空白を整理
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    # 空白行を除去
                    scraped_data = [chunk for chunk in chunks if chunk]
            
            except requests.exceptions.RequestException as e:
                error = f"リクエストエラー: {str(e)}"
            except Exception as e:
                error = f"エラーが発生しました: {str(e)}"
    
    return render_template('index.html', scraped_data=scraped_data, error=error, url=url)

if __name__ == '__main__':
    app.run(debug=True) 