import pandas as pd

df = pd.read_csv('datasets/cars_db_04_10.11.csv')
print(df.isna().sum())