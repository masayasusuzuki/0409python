from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import google.generativeai as genai

app = Flask(__name__)

# Gemini APIの設定
GEMINI_API_KEY = "AIzaSyAtj18gUum2qZ6jrE-S-MpGGdwtltpIF1k"
genai.configure(api_key=GEMINI_API_KEY)

# 最新のGemini 2.5 Proプレビューモデルを使用
model = genai.GenerativeModel('gemini-2.5-pro-preview-03-25')

def summarize_text(text_content):
    """Gemini APIを使用してテキストを要約する関数"""
    try:
        # テキストコンテンツを結合して一つの文字列にする
        if isinstance(text_content, list):
            combined_text = "\n".join(text_content)
        else:
            combined_text = text_content
            
        # テキストが長すぎる場合は適切な長さに切り詰める（APIの制限に対応）
        if len(combined_text) > 100000:  # 10万文字程度で制限
            combined_text = combined_text[:100000]
        
        # 要約のプロンプト
        prompt = f"""以下のウェブページの内容を要約し、読みやすいレジュメ形式にしてください。

        ===フォーマット仕様===
        1. タイトル: ウェブページの主要テーマに基づいたタイトルをつけてください（H2タグ使用）
        2. 概要: 100文字程度で全体の概要を説明してください（ここだけ読めば内容が把握できるように）
        3. 主なポイント: 箇条書きで3〜5つの重要ポイントを挙げてください
        4. 詳細: 主なポイントの詳細をそれぞれ説明してください（50-100文字程度）
        5. 結論: 内容の結論や重要な示唆を説明してください

        出力はHTMLフォーマットで行い、適切なタグ（h2, h3, p, ul, li等）を使用して構造化してください。
        
        ウェブページの内容:
        {combined_text}"""
        
        # 要約の生成
        response = model.generate_content(prompt)
        
        # レスポンスからテキストを取得
        summary = response.text
        return summary
    
    except Exception as e:
        return f"要約の生成中にエラーが発生しました: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    scraped_data = None
    summary = None
    error = None
    url = ""
    
    if request.method == 'POST':
        url = request.form.get('url')
        selector = request.form.get('selector', '')
        summarize = request.form.get('summarize') == 'on'
        
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
                
                # 要約オプションが選択されている場合は要約を生成
                if summarize and scraped_data:
                    summary = summarize_text(scraped_data)
            
            except requests.exceptions.RequestException as e:
                error = f"リクエストエラー: {str(e)}"
            except Exception as e:
                error = f"エラーが発生しました: {str(e)}"
    
    return render_template('index.html', scraped_data=scraped_data, summary=summary, error=error, url=url)

# API経由で要約を取得するエンドポイント
@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    data = request.json
    text_content = data.get('text', '')
    
    if not text_content:
        return jsonify({"error": "テキストが提供されていません"}), 400
    
    summary = summarize_text(text_content)
    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True) 