# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ec
import numpy as np
import matplotlib.pyplot as plt
import os

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

# featuredArticleList = ['Arabian_Sea.xml']

def CurrentText(articleName):
	try:
		tree = ec.parse(articleName) 
		root = tree.getroot()

		pageElement = root[1]

		latestRevisionText = ''
		for child in pageElement:
			if 'revision' in child.tag:
				for each in child:
					if 'text' in each.tag:
						latestRevisionText = each.text

		return latestRevisionText
	except:
		print('\n'+'Error! in parsing '+articleName+'\n')
		return -1

def NumberOfImages(currentText, articleName):
	imageFormates = ['.jpg','.jpeg','.svg','.gif','.png','.bmp','.tiff']
	try:
		count = 0
		for image in imageFormates:
			count += currentText.count(image)	
		print(articleName + ' ' + str(count))	
		return count

	except:
		print('\n'+'Something went wrong!'+articleName+'\n')
		return -1

def main():
    listOfImagesFA = []
    listOfImagesGA = []
    xAxis = []
    sc = []
    count=1
    for articleName in featuredArticleList: 
        currentText =  CurrentText(articleName)
        if currentText != -1:
            listOfImagesFA.append(NumberOfImages(currentText, articleName))
            xAxis.append(count)
            sc.append(5)
            count+=1

    listOfImagesFA.sort()
    for articleName in goodArticleList: 
        currentText =  CurrentText(articleName)
        if currentText != -1:
            listOfImagesGA.append(NumberOfImages(currentText, articleName))

    listOfImagesGA.sort()

    plt.xlabel('Articles', fontsize=12)
    plt.ylabel('Number of Images', fontsize=12)
    plt.scatter(xAxis,listOfImagesFA, c='b',s=sc, marker='o',label='Number Of Images in FA')
    plt.scatter(xAxis,listOfImagesGA, c='r',s=sc, marker='^',label='Number Of Images in GA')
    plt.legend()
    plt.savefig('numberOfImages.png',dpi=800)
    plt.show()	
    #npArray = np.array(listOfImages)
    #print('Mean number of Images ' + str(np.mean(npArray)))
    #print('Standard Deviation ' + str(np.std(npArray)) + '\n')

main()