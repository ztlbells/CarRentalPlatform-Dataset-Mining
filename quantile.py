# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 21:20:04 2016

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

q=[[]]
targetFile=file(r"E:\quant.csv","wb")
writer=csv.writer(targetFile,quoting=csv.QUOTE_ALL)

test_quantile =0.25
iterator = 0

##search for the best @param test_quantile for the highest silh_score
## quantile : 0~1 , but 0.25~0.76 is a better range 
while test_quantile < 0.76:
    print "====="
    print "quantile="+str(test_quantile)
    bandwidth = estimate_bandwidth(X, quantile=test_quantile)
    print "bandwidth="+str(bandwidth)
    
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    print "n_clusters_="+str(n_clusters_)
    
    sil_score =str(metrics.silhouette_score(X,labels,metric = 'euclidean'))
    print "silh_score:"+str(sil_score)
    
    if iterator == 0:
        q[0]=[str(test_quantile),str(n_clusters_),sil_score]
        writer.writerow(q[0])
    else:
        q.append([str(test_quantile),str(n_clusters_),sil_score])
        writer.writerow(q[iterator])
        
    test_quantile=test_quantile+0.01
    iterator=iterator+1

csvFile.close();
targetFile.close();