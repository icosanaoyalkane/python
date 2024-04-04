import os
import pandas as pd

# user input
dir_path = r"C:\Users\1002789-Z100.GLOBAL\Desktop\0125_all.csv"

# dir name & File name
dirname = os.path.dirname(dir_path)
filename = os.path.splitext(os.path.basename(dir_path))[0]
ext = os.path.splitext(os.path.basename(dir_path))[1]
output_dir = os.path.join(dirname, filename)
os.mkdir(output_dir)



# pandas
df = pd.read_csv(dir_path)
x = df['x']
y = df.drop('x', axis=1)

# join
columns_list = y.columns.values.tolist()
for i in columns_list:
    df2 = pd.concat([x, y[i]], axis=1)
    i_filename = i + ext
    output_file = os.path.join(output_dir,i_filename)
    df2.to_csv(output_file, header=False, index=False)

# print(df)
