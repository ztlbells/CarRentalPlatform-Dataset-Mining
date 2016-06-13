# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 16:30:05 2016

"""
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
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
    new_element=[float(line[1]),float(line[2]),float(line[3])]#,float(line[4]),float(line[5]),float(line[6]),float(line[7]),float(line[8])]
    if reader.line_num == 2:
        X[0]=new_element
    else:
        X.append(new_element)
        
        
#normalization
X = StandardScaler().fit_transform(X)

#pca
pca = PCA(n_components=2)
X = pca.fit_transform(X)
print X


# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
bandwidth = estimate_bandwidth(X, quantile=0.3)

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

# Plot result
import matplotlib.pyplot as plt
from itertools import cycle

plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], '.', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()