# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ec
import numpy as np
import os
import matplotlib.pyplot as plt

path = os.getcwd()
path1 = path + '/wiki_data/FA/'
path2 = path + '/wiki_data/GA/'
FAfilenames = os.listdir(path1)
GAfilenames = os.listdir(path2)

featuredArticleList = []
goodArticleList = []

for filename in FAfilenames:
    if '.xml' in filename:
        filename = path1 + filename
        featuredArticleList.append(filename)        
        
for filename in GAfilenames:
    if '.xml' in filename:
        filename = path2 + filename
        goodArticleList.append(filename)        

#featuredArticleList = ['International Mathematical Olympiad.xml']

def NumberOfReverts(articleName):
	# try:
		tree = ec.parse(articleName) 
		root = tree.getroot()

		pageElement = root[1]
		total = 0
		reverts = {}

		for child in pageElement:
			if 'revision' in child.tag:
				for each in child:
					if 'sha1' in each.tag:
						sha1Value = each.text
						try:
							if reverts[sha1Value]:
								reverts[sha1Value] += 1
								total += 1
						except:
							reverts[sha1Value] = 1

		for key in reverts:
			if reverts[key] >= 2:
				print(key, reverts[key]) 

		print(articleName + ' ' + str(total))
		return total
	# except:
	# 	print('\n'+'Error! '+articleName+'\n')
	# 	return -1

def main():
    listOfRevertsFA = []
    listOfRevertsGA = []
    xAxis = []
    sc = []
    count=1
    for articleName in featuredArticleList: 
        result = NumberOfReverts(articleName)
        if result != -1:
            listOfRevertsFA.append(result)
            xAxis.append(count)
            count+=1
            sc.append(5)
    
    listOfRevertsFA.sort()

    for articleName in goodArticleList: 
        result = NumberOfReverts(articleName)
        if result != -1:
            listOfRevertsGA.append(result)

    plt.xlabel('Articles', fontsize=12)
    plt.ylabel('Number of Revertss', fontsize=12)
    plt.scatter(xAxis,listOfRevertsFA, c='b',s=sc, marker='o',label='Number Of Reverts in FA')
    plt.scatter(xAxis,listOfRevertsGA, c='r',s=sc, marker='^',label='Number Of Reverts in GA')
    plt.legend()
    plt.savefig('numberOfReverts.png',dpi=800)
    plt.show()	

    #npArrayFA = np.array(listOfRevertsFA)
    #npArrayGA = np.array(listOfRevertsGA)
    #print('Mean Value of all articles ' + str(np.mean(npArray)))
    #print('Standard Deviation ' + str(np.std(npArray)))

main()