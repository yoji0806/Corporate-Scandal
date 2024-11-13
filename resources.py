from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime, timezone, timedelta
import pandas as pd




def df_google_news_from_to(date_before, date_after, keyword):
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






date_from_str = "2020-01-01"
date_to_str = "2024-11-13"
keywords = ["不祥事", "不正"]


date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
date_to = datetime.strptime(date_to_str, '%Y-%m-%d')

columns = ['title', 'date', 'url']
df_result = pd.DataFrame(columns=columns)

# 1週間ごとのループを回す
date_before = date_to
while date_before > date_from:

    date_after = date_before - timedelta(weeks=1)

    date_after_str = date_after.strftime('%Y-%m-%d')
    date_before_str = date_before.strftime('%Y-%m-%d')

    for keyword in keywords:
        df_scandals = df_google_news_from_to(date_before_str, date_after_str, keyword)

        df_result = pd.concat([df_result, df_scandals], ignore_index=True)
        print(f"{date_before_str} - {date_after_str}: {df_scandals.shape[0]}件（合計： {df_result.shape[0]}件） keyword: {keyword}")


    date_before = date_after



df_result.to_csv('scandals_20200101_20241113.csv', index=False, encoding='utf-8')



