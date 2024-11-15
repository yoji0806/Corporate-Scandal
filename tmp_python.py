
import pandas as pd

scandal_df = pd.read_csv("./data/scandals_20200101_20241113.csv")

print(scandal_df.loc[0])
