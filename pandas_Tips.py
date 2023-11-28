import pandas as pd

df = pd.DataFrame([
    [1, 'Taro', 12],
    [2, 'Yoshiko', 25],
    [3, 'Hanako', 18],
    [4, 'Santa', 25],
    [5, 'Nobu', 16],
    [6, 'Haruka', 29]],
    columns=['id','name','score']
)


#read csv ---------------
df = pd.read_csv("file:/tmp/covid.csv")
df = pd.read_csv(i, encoding='shift_jis') #encording

#shape ---------------
print(df.shape)

#graph split point ---------------
df['TG(mg)dif'] = df['TG(mg)'].diff().abs()
split_point = pd.concat([df[(df['TG(mg)dif'] > 0.1) &  (df['TG(mg)'] < 0.001)], df.tail(1)])
split_index = split_point.index.values.tolist()

#split -> output loop ---------------
for j in range(len(split_index)):
    if j == 0:
        #split
        df_i = df.iloc[:split_index[j], :]
        df_i = df_i.reset_index(drop=True)

        #Time(min) reset
        df_i['Time(min)'] = df_i['Time(min)'] - df_i.at[df_i.index[0], 'Time(min)']
        
        #output as csv
        c = title + '-' + str(j) + '.csv'
        tx = os.path.join(OUT, c)
        df_i.to_csv(tx, encoding='shift_jis', na_rep=0)

    else:
        #split
        df_i = df.iloc[split_index[j-1]:split_index[j], :]
        df_i = df_i.reset_index(drop=True)

        #Time(min) reset
        df_i['Time(min)'] = df_i['Time(min)'] - df_i.at[df_i.index[0], 'Time(min)']

        #output as csv
        c = title + '-' + str(j) + '.csv'
        tx = os.path.join(OUT, c)
        df_i.to_csv(tx, encoding='shift_jis', na_rep=0)
