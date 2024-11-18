from datetime import datetime, timedelta
import pandas as pd
import utils





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
        df_scandals = utils.df_google_news_from_to(date_before_str, date_after_str, keyword)

        df_result = pd.concat([df_result, df_scandals], ignore_index=True)
        print(f"{date_before_str} - {date_after_str}: {df_scandals.shape[0]}件（合計： {df_result.shape[0]}件） keyword: {keyword}")


    date_before = date_after



df_result = df_result.drop_duplicates()

df_result.to_csv('scandals_20200101to20241113.csv', index=False, encoding='utf-8')



