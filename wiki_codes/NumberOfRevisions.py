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
        # filename = path + filename
        featuredArticleList.append(path1+filename)

for filename in GAfilenames:
    if '.xml' in filename:
        # filename = path + filename
        goodArticleList.append(path2+filename)

# featuredArticleList = ['Arabian_Sea.xml']

def NumberOfRevisions(articleName):
	try:
		tree = ec.parse(articleName) 
		root = tree.getroot()

		pageElement = root[1]
		count = 0

		for child in pageElement:
			if 'revision' in child.tag:
				count += 1

		print(articleName + ' ' + str(count))
		return count
	except:
		print('\n'+'Error! '+articleName+'\n')
		return -1

def main():
    listOfResultsFA = []
    listOfResultsGA = []
    xAxis = []
    sc = []
    count=1
    for articleName in featuredArticleList: 
        result = NumberOfRevisions(articleName)
        if result != -1:
            listOfResultsFA.append(result)
            xAxis.append(count)
            count+=1
            sc.append(5)
            
    listOfResultsFA.sort()
    
    for articleName in goodArticleList: 
        result = NumberOfRevisions(articleName)
        if result != -1:
            listOfResultsGA.append(result)

    listOfResultsGA.sort()

    plt.xlabel('Articles', fontsize=12)
    plt.ylabel('Number of Sections', fontsize=12)
    plt.scatter(xAxis,listOfResultsFA, c='b',s=sc, marker='o',label='Number Of revisions in FA')
    plt.scatter(xAxis,listOfResultsGA, c='r',s=sc, marker='^',label='Number Of revisions in GA')
    plt.legend()
    plt.savefig('numberOfRevisions.png',dpi=800)
    plt.show()	
    #npArray = np.array(listOfResults)
    #print('Mean Value of all articles ' + str(int(np.mean(npArray))))
    #print('Standard Deviation ' + str(np.std(npArray)))

main()