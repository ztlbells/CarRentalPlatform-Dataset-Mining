# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 19:55:14 2016

@author: zutianluo
"""
import numpy as np
from sklearn.cluster import KMeans
import csv
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

#X is the data set
X=[[]]

#import data from orig dataset
csvFile=file(r"E:\new.csv","rb")
reader=csv.reader(csvFile)
for line in reader:
    #ignore first line
    if reader.line_num == 1:
        continue
    new_element=[float(line[1]),float(line[2]),float(line[3]),float(line[4]),float(line[5]),float(line[6]),float(line[7]),float(line[8])]
    if reader.line_num == 2:
        X[0]=new_element
    else:
        X.append(new_element)
        
        
#normalization
X = StandardScaler().fit_transform(X)

#pca
pca = PCA(n_components=2)
X = pca.fit_transform(X)
#print X

db = KMeans(n_clusters=8, random_state=1).fit(X)
print db
labels = db.labels_ 
print "silh_score:"+str(metrics.silhouette_score(X,labels,metric = 'euclidean'))
db = KMeans(n_clusters=5, random_state=1).fit_predict(X)
plt.scatter(X[:, 0], X[:, 1], c=db, marker='o',alpha = 0.3, edgecolors = 'None')
plt.title('Predetermined number of clusters: %d' % 8)
plt.show()