
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from openai import OpenAI
import requests
import re
import pandas as pd





def df_google_news_from_to(date_before: str, date_after: str, keyword: str) -> pd.DataFrame:
    """
    Google Newsで、特定の日付範囲とキーワードの検索結果をdfで返す。

    Args:
        date_before (str): yyyy-mm-dd, 日付範囲の初め
        date_after (str): yyyy-mm-dd, 日付範囲の終わり
        keyword (str): 検索ワード

    Returns:
        df_articles (dataframe): 3つの列（title, date, url）を持つデータフレーム 
    """
    str_blank = '%E3%80%80'
    str_colon = '%3A'

    url = f'https://news.google.com/search?q={keyword}{str_blank}after{str_colon}{date_after}{str_blank}before{str_colon}{date_before}&hl=ja&gl=JP&ceid=JP{str_colon}ja'

    # 記事の情報を抽出する正規表現
    re_googlenews = r'\[\[13,.*?"([^"]+)",null,\[(\d+)\],null,"(https?://.*?)",'
    articles = []

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')  

    # 記事を含む全ての要素を探索
    matches = soup.find_all(string=re.compile(re_googlenews))


    # 各記事情報を抽出
    for match in matches:
        articles_raw = re.findall(re_googlenews, match)

        for article in articles_raw:
            title = article[0]
            timestamp = int(article[1])
            url = article[2]
            
            # タイムスタンプを日本標準時に変換
            publish_date = datetime.fromtimestamp(timestamp, timezone(timedelta(hours=9))).strftime('%Y-%m-%d %H:%M:%S')

            articles.append({
                'title': title,
                'date': publish_date,
                'url': url
            })

    df_articles = pd.DataFrame(articles)

    return df_articles





def get_stock_code(keyword: str) -> int:
    """
    カブタンで、キーワードで検索して合致した場合にその企業銘柄を返す

    Args:
        keyword (str): 検索ワード

    Returns:
        stock_code (int): 4桁の数字。見つからない場合は0を返す
    """

    base_url = "https://kabutan.jp/search/"
    search_url = f"{base_url}?q={keyword}"
    response = requests.get(search_url)
    
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    stock_code = None

    for link in soup.find_all('a', href=True):
        if link['href'].startswith('/search/linkcompany?code='):
            match = re.search(r'code=(\d+)', link['href'])
            if match:
                stock_code = match.group(1)
                break

    if not stock_code:
        stock_code = 0
    
    return stock_code



def call_openai_basic(instruction: str, prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    openAI のAPI呼び出し
    詳しい使い方は、https://platform.openai.com/docs

    Args:
        instruction (str): 検索ワード
        prompt (str): 
        model (str): chatGPTのモデル

    Returns:
        reuslt (str): AIの応答結果
    """

    client = OpenAI()
    completion = client.chat.completions.create(
        model = model,
        messages=[
            {"role": "system", "content": instruction},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    print(completion.choices[0].message)
    
    return completion.choices[0].message