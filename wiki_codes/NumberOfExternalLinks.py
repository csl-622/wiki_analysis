# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ec
import requests
import os
import numpy as np
import mwparserfromhell
import matplotlib.pyplot as plt

path = os.getcwd()
path1 = path + '/wiki_data/FA'
path2 = path + '/wiki_data/GA'
filenamesFA = os.listdir(path1)
filenamesGA = os.listdir(path2)

featuredArticleList = []
goodArticleList = []

for filename in filenamesFA:
    if '.xml' in filename:
        filename = path1+'/' + filename
        featuredArticleList.append(filename)

for filename in filenamesGA:
    if '.xml' in filename:
        filename = path2+'/' + filename
        goodArticleList.append(filename)
# featuredArticleList = ["Death Is Birth.xml"]

def ExternalLinks(articleName):
	try:
		tree = ec.parse(articleName) 
		root = tree.getroot()

		pageElement = root[1]
		latestText = ''

		for child in pageElement:
			if 'revision' in child.tag:
				for each in child:
					if 'text' in each.tag:
						try:
							sizeOfArticle = int(each.attrib['bytes'])
							latestText = each.text
						except:
							continue

		# print(latestText)
		wikicode = mwparserfromhell.parse(latestText)
		count = 0
		for each in wikicode.filter_external_links():
			count += 1

		print(articleName + ' ' + str(count))
		return count

	except:
		print('\n'+'Error! in parsing '+articleName+'\n')
		return -1

def main5():
    ExternalLinksListFA = []
    ExternalLinksListGA = []
    xAxis = []
    count=1
    sc = []
    for articleName in featuredArticleList:
        result = ExternalLinks(articleName)
        if result != -1:
            ExternalLinksListFA.append(result)
            xAxis.append(count)
            count+=1
            sc.append(5)
            
    ExternalLinksListFA.sort()

    for articleName in goodArticleList:
        result = ExternalLinks(articleName)
        if result != -1:
            ExternalLinksListGA.append(result)

    ExternalLinksListGA.sort()

    plt.xlabel('Articles', fontsize=12)
    plt.ylabel('Number of External Links', fontsize=12)
    plt.scatter(xAxis,ExternalLinksListFA, c='b',s=sc, marker='o',label='Number Of External Links in FA')
    plt.scatter(xAxis,ExternalLinksListGA, c='r',s=sc, marker='^',label='Number Of External Links in GA')
    plt.legend()
    plt.savefig('numberOfExternalLinks.png',dpi=800)
    plt.show()    

    #ExternalLinksList = np.array(ExternalLinksList)
    #print(str(np.mean(ExternalLinksList)) + ' ' + str(np.std(ExternalLinksList)))

main5()