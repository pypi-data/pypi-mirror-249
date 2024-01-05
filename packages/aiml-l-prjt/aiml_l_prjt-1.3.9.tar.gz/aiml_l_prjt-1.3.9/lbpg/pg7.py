#Em algo
# import matplotlib.pyplot as plt
# from sklearn import datasets
# from sklearn.cluster import KMeans
# import pandas as pd
# import numpy as np

dt=datasets.load_iris()
x=pd.DataFrame(dt.data)
x.columns=["sepal_Length","Sepal_Width","Petal_Lengt","Petal_Width"]
y=pd.DataFrame(dt.target)
y.columns=["target"]
plt.figure(figsize=(14,14))
mode=KMeans(n_clusters=3)
color=np.array(["Red","Blue","black"])
mode.fit(x)
plt.subplot(2,2,1)
plt.scatter(x.Petal_Lengt,x.Petal_Width,c=color[y.target],s=40)
plt.title("Normal")
plt.xlabel("width")
plt.ylabel("lehgth")

plt.subplot(2,2,2)
plt.scatter(x.Petal_Lengt,x.Petal_Width,c=color[mode.labels_],s=40)
plt.title("Normmmal")
plt.xlabel("width")
plt.ylabel("lehgth")

from sklearn import preprocessing
sc=preprocessing.StandardScaler()
sc.fit(x)
ii=sc.transform(x)
sss=pd.DataFrame(ii,columns=x.columns)
from sklearn.mixture import GaussianMixture
e=GaussianMixture(n_components=3)
e.fit(sss)
val=e.predict(sss)

plt.subplot(2,2,3)
plt.scatter(x.Petal_Lengt,x.Petal_Width,c=[val],s=40)
plt.title("Normal")
plt.xlabel("width")
plt.ylabel("lehgth")
