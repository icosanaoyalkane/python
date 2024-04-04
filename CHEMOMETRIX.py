import pandas
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

filename = r"C:\Users\1002789-Z100.GLOBAL\Desktop\DRY.csv"
Dim = 2

# スペクトルデータ読み込み→転置してデータセット化
spec = pandas.read_csv(filename, header=0, index_col=0).T
spec.T.plot(legend=None)
print(spec)

# 主成分分析(次元削減)
pca = PCA(n_components=Dim).fit(spec)
print(pca.explained_variance_ratio_)

# 成分はどこのスペクトル波数をみているか
loading = pandas.DataFrame(pca.components_, columns=spec.columns)
#loading.T.plot()
loading.T.to_csv(filename[:-4]+'_loading.csv')
print(loading)

# 各成分で分ける
score = pandas.DataFrame(pca.transform(spec), index=spec.iloc[:,0])
#score.plot()
score.to_csv(filename[:-4]+'_score.csv')

# グラフ
fig, ax = plt.subplots()
ax.scatter(score.iloc[:,0], score.iloc[:,1], c=spec.iloc[:,0], cmap=plt.get_cmap('Blues') )

# #データラベル
for i, label in enumerate(spec.index):
    ax.text(score.iloc[i,0], score.iloc[i,1],label)

plt.show()
