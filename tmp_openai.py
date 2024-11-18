import pandas as pd
import os
import json
import utils
import time
from datetime import datetime


start_time = time.time()


with open("./apikey_openai.txt", "r") as file:
    apikey_openai = file.read().strip()
    os.environ["OPENAI_API_KEY"] = apikey_openai

with open("./instruction_toLLM/extract_scandal_company_name.txt", "r") as file:
    instruction = file.read().strip()


scandal_df = pd.read_csv("./data/scandals_20200101to20241113.csv")
article_ls = scandal_df["title"].to_list()

article_numbered_ls = [f"{i}.{item}" for i, item in enumerate(article_ls)]

batch_size = 100

# wip
start_line = 700
scandal_df = scandal_df.iloc[start_line:]

try:
    for i in range(0, len(article_ls), batch_size):
        batch_ls = article_numbered_ls[i:i+batch_size]

        result_chat = utils.call_openai_basic(instruction, prompt=str(batch_ls), model="gpt-4o")
        result_str = result_chat.content

        if result_str.startswith("```json"):
            result_str = result_str[7:-3]

        result_json = json.loads(result_str)

        for item in result_json:
            row_index = int(item['no']) 
            scandal_df.loc[row_index, 'scandal_of_company'] = item['s_c']
            scandal_df.loc[row_index, 'company_name'] = item['n']
            scandal_df.loc[row_index, 'related_company_name'] = item['nn']

        rap = time.time()
        elapsed_time = rap - start_time
        print(f"{i} 回目のバッチ終了！：{elapsed_time:.2f} s : {datetime.now()}")

        start_time = time.time()


except Exception as e:
    scandal_df.to_csv("scandal_df_partial_output.csv", index=False)
        # 処理時間を測定
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Error was captured!!!")
    print(e)
    with open("error_.txt", "w") as file:
        file.write(result_str)


scandal_df.to_csv("./data/scandals_20200101to20241113_symbol_added", index=False)

# 処理時間を測定
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Processing time: {elapsed_time:.2f} seconds")





