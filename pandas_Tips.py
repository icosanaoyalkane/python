import pandas as pd

#read csv
df = pd.read_csv("file:/tmp/covid.csv")
df = pd.read_csv(i, encoding='shift_jis') #encording

#shape
print(df.shape)
