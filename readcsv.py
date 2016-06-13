# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 10:59:53 2016

@author: zutianluo
"""

import csv

csvFile=file("E:\source.csv","rb")
targetFile=file(r"E:\new.csv","wb")

reader=csv.reader(csvFile)
writer=csv.writer(targetFile,quoting=csv.QUOTE_ALL)

writer.writerow(['ID','total_csm','act_deg','age'])

for line in reader:
    if reader.line_num == 1:
        continue
    #writer.writerow(line)
        
    ##total_consumption
    if float(line[1])*float(line[3])-float(line[4]) < 0.0:
        total_csm = 0.0
    else :
        total_csm = float(line[1])*float(line[3])-float(line[4])
  
    ##degree of activity
    act_deg = float(line[1])*0.3 + float(line[2])*0.3 + float(line[4])*0.1 + float(line[8])*0.3

    ##ages
    print str(reader.line_num)+":"+line[5] + "," + line[6]
    age = float(line[5])*0.5 + float(line[6])*0.5
    
    
    ##output :      ID      csm            act          age
    writer.writerow([line[0],str(total_csm),str(act_deg),age])
    
csvFile.close();
targetFile.close();
