# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ec
import numpy as np
import os

path = os.getcwd()
# path = path + '/WikiData/GoodArticles/'
filenames = os.listdir(path)

featuredArticleList = []
for filename in filenames:
    if '.xml' in filename:
        # filename = path + filename
        featuredArticleList.append(filename)   

# featuredArticleList = ['Arabian_Sea.xml']     

def NumberOfReverts(articleName):
	try:
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
								total += 1
						except:
							reverts[sha1Value] = 1


		print(articleName + ' ' + str(total))
		return total
	except:
		print('\n'+'Error! in parsing '+articleName+'\n')
		return -1

def main():
	listOfReverts = []
	for articleName in featuredArticleList: 
		result = NumberOfReverts(articleName)
		if result != -1:
			listOfReverts.append(result)

	npArray = np.array(listOfReverts)
	print('Mean number of reverts ' + str(np.mean(npArray)))
	print('Standard Deviation ' + str(np.std(npArray)))

main()