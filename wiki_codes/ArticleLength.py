# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ec
import numpy as np
import os

path = '/home/descentis/research/WikiMeter/analysis/wiki_analysis/wiki_data'
# path = path + '/WikiData/GoodArticles/'
filenames = os.listdir(path)

featuredArticleList = []
for filename in filenames:
    if '.xml' in filename:
        filename = path+'/'+filename
        featuredArticleList.append(filename)

# featuredArticleList = ['Arabian_Sea.xml']

def ArticleLength(articleName):
	try:
		tree = ec.parse(articleName) 
		root = tree.getroot()

		pageElement = root[1]
		total = 0
		contributors = {}

		for child in pageElement:
			if 'revision' in child.tag:
				for each in child:
					if 'text' in each.tag:
						try:
							sizeOfArticle = int(each.attrib['bytes'])
						except:
							continue

		print(articleName + ' ' + str(sizeOfArticle))

		if sizeOfArticle != 0:
			return sizeOfArticle
		else:
			return -1

	except:
		print('\n'+'Error! in parsing '+articleName+'\n')
		return -1

def main():
	listOfResults = []
	for articleName in featuredArticleList: 
		result = ArticleLength(articleName)
		if result != -1:
			listOfResults.append(result) 

	npArray = np.array(listOfResults)
	print('Mean Value of all articles ' + str(np.mean(npArray)))
	print('Standard Deviation ' + str(np.std(npArray)))

main()