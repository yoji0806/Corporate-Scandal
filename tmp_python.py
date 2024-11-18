import pandas as pd


scandal_df = pd.read_csv("./data/scandals_20200101to20241113.csv")

start_line = 700
scandal_df = scandal_df.iloc[start_line]

print(scandal_df.head(10))