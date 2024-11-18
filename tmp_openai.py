from pydantic import BaseModel
import pandas as pd
import os
import json
import utils
import time
from openai import OpenAI


start_time = time.time()


with open("./apikey_openai.txt", "r") as file:
    apikey_openai = file.read().strip()
    os.environ["OPENAI_API_KEY"] = apikey_openai

with open("./instruction_toLLM/extract_scandal_company_name.txt", "r") as file:
    instruction = file.read().strip()


class scandalous_coumpany(BaseModel):
    no: int
    s_c: str
    n: str
    nn: str

class Inspectation(BaseModel):
    final_result: list[scandalous_coumpany]




scandal_df = pd.read_csv("./data/scandals_20200101to20241113.csv")
done_df = pd.read_csv("./data/done.csv")

scandal_df = scandal_df[~scandal_df["title"].isin(done_df["title"])]
scandal_df = scandal_df.reset_index(drop=True)

article_ls = scandal_df["title"].to_list()
article_numbered_ls = [f"{i}.{item}" for i, item in enumerate(article_ls)]

batch_size = 100


try:
    for i in range(0, len(article_ls), batch_size):
        batch_ls = article_numbered_ls[i:i+batch_size]

        result_raw = utils.call_openai_structured_output(
                instruction= instruction,
                prompt= str(batch_ls),
                model = "gpt-4o",
                response_format= Inspectation
        )

        result_inspection = result_raw.final_result

        for item in result_inspection:
            row_index = item.no
            scandal_df.loc[row_index, 'scandal_of_company'] = item.s_c
            scandal_df.loc[row_index, 'company_name'] = item.n
            scandal_df.loc[row_index, 'related_company_name'] = item.nn

        

        # result_str = utils.call_openai_basic(instruction, prompt=str(batch_ls), model="gpt-4o")
        # result_str = result_str.content

        # chatGPTの表記揺れの修正
        # if result_str.startswith("```json"):
        #     result_str = result_str[7:-3]

        # if result_str.startswith("\n"):
        #     result_str = result_str[1:]
        
        # if result_str.startswith("\n"):
        #     result_str = result_str[1:]

        # if result_str.endswith("\n`"):
        #     result_str = result_str[:-2]

        #result_json = json.loads(result_str)

        # for item in result_json:
        #     row_index = int(item['no']) 
        #     scandal_df.loc[row_index, 'scandal_of_company'] = item['s_c']
        #     scandal_df.loc[row_index, 'company_name'] = item['n']
        #     scandal_df.loc[row_index, 'related_company_name'] = item['nn']

        rap = time.time()
        elapsed_time = rap - start_time
        print(f"{i} 回目のバッチ終了！：{elapsed_time:.2f} s")

        start_time = time.time()

        1 + "a"


except Exception as e:
    scandal_df.to_csv("scandal_df_partial_output.csv", index=False)
        # 処理時間を測定
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Error was captured!!!")
    print(e)


scandal_df.to_csv("./data/scandals_20200101to20241113_symbol_added.csv", index=False)

# 処理時間を測定
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Processing time: {elapsed_time:.2f} seconds")



