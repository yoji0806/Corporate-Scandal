import pandas as pd
from openai import OpenAI
import os

df = pd.read_csv("./scandals_20200101_20241113.csv")
ls = df["title"].to_list()

print(ls[:10])