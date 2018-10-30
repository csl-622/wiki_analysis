# -*- coding: utf-8 -*-

#THIS IS WRONG!!! USE WIKIMEDIA API TO GET FETCH THE SECTIONS AND THEN COUNT IT.

import xml.etree.cElementTree as ec
import os
import mwparserfromhell
import matplotlib.pyplot as plt

path = os.getcwd()
path1 = path+'/wiki_data/FA/'
path2 = path+'/wiki_data/GA/'
FAfilenames = os.listdir(path1)
GAfilenames = os.listdir(path2)

featuredArticleList = []
goodArticleList = []

for filename in FAfilenames:
    if '.xml' in filename:
        featuredArticleList.append(path1+filename)

for filename in GAfilenames:
    if '.xml' in filename:
        goodArticleList.append(path2+filename)

# featuredArticleList = ['Arabian_Sea.xml']

def NumberOfSections(articleName):
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
							latestText = each.text
						except:
							continue

		wikicode = mwparserfromhell.parse(latestText)
		count = len(wikicode.get_sections())
		print(articleName + ' ' + str(count))
		return count

	except:
		print('\n'+'Error! in parsing '+articleName+'\n')
		return -1


def main():
    xAxis = []
    NumberOfSectionsListFA = []
    NumberOfSectionsListGA = []
    sc = []
    count=1
    for articleName in featuredArticleList:
        result = NumberOfSections(articleName)
        if result != -1:
            NumberOfSectionsListFA.append(result)
            xAxis.append(count)
            count+=1
            sc.append(5)
    
    NumberOfSectionsListFA.sort()

    for articleName in goodArticleList:
        result = NumberOfSections(articleName)
        if result != -1:
            NumberOfSectionsListGA.append(result)
    
    NumberOfSectionsListGA.sort()
    
    plt.xlabel('Articles', fontsize=12)
    plt.ylabel('Number of Sections', fontsize=12)
    plt.scatter(xAxis,NumberOfSectionsListFA, c='b',s=sc, marker='o',label='Number Of sections in FA')
    plt.scatter(xAxis,NumberOfSectionsListGA, c='r',s=sc, marker='^',label='Number Of sections in GA')
    plt.legend()
    plt.savefig('numberOfSections.png',dpi=800)
    plt.show()

    #NumberOfSectionsList = np.array(NumberOfSectionsList)
    #print('Sections ' + str(np.mean(NumberOfSectionsList)) + ' ' + str(np.std(NumberOfSectionsList)))

main()