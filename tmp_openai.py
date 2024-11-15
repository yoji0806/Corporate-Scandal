import pandas as pd
import os
import json
import utils



with open("./apikey_openai.txt", "r") as file:
    apikey_openai = file.read().strip()
    os.environ["OPENAI_API_KEY"] = apikey_openai

with open("./instruction_toLLM/extract_scandal_company_name.txt", "r") as file:
    instruction = file.read().strip()


scandal_df = pd.read_csv("./data/scandals_20200101to20241113.csv")
article_ls = scandal_df["title"].to_list()

article_numbered_ls = [f"{i}.{item}" for i, item in enumerate(article_ls)]

batch_size = 100
for i in range(0, len(article_ls), batch_size):
    batch_ls = article_numbered_ls[i:i+batch_size]

    result_str = utils.call_openai_basic(instruction, prompt=str(batch_ls), model="gpt-4o")

    result_json = json.loads(result_str)

    for item in result_json:
        row_index = int(item['no']) 
        scandal_df.loc[row_index, 'scandal_of_company'] = item['s_c']
        scandal_df.loc[row_index, 'company_name'] = item['n']
        scandal_df.loc[row_index, 'related_company_name'] = item['nn']


scandal_df.to_csv("./data/scandals_20200101to20241113_symbol_added")





