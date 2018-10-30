    # -*- coding: utf-8 -*-
    
import xml.etree.cElementTree as ec
import matplotlib.pyplot as plt
import os
from FeaturedDate import GetFeaturedArticleDate 

path = os.getcwd()
path = path+'/wiki_data'
filenames = os.listdir(path)

featuredArticleList1 = []
featuredArticleList2 = []
for filename in filenames:
    if '.xml' in filename:
        featuredArticleList1.append(filename)
        featuredArticleList2.append(path+'/'+filename)

#featuredArticleList = ['/home  /descentis/research/WikiMeter/analysis/wiki_analysis/wiki_data/Zinc.xml']
    
def PlotChangeInSizeGraph(articleName, FeaturedDate,num):
    tree = ec.parse(articleName) 
    root = tree.getroot()
    
    pageElement = root[1]
    	#print pageElement
    
    SizeOfArticle = 0
    ChangeInArticle = 0
    MaxChange = 0
    MaxChangeDate = ''
    previousSize = 0
    PastChangeInSize = 0
    dateTemp = 0
    Pastdate = 0
    count = 0
    error = 0
    yAxis = []
    xAxis = []
    
    for child in pageElement:
        if 'revision' in child.tag: 
            for each in child:
                if 'timestamp' in each.tag:
                    dateTemp = int(each.text[0:10].replace('-', ''))
    
                if 'text' in each.tag:
                    if(each.attrib.get('bytes')!=None):
                        SizeOfArticle = int(each.attrib['bytes'])
                        ChangeInArticle = SizeOfArticle - previousSize
                        tempCalc = int(0.1*abs(PastChangeInSize))
                        if abs(ChangeInArticle) in range(abs(PastChangeInSize)-tempCalc, abs(PastChangeInSize)+tempCalc+1) and abs(ChangeInArticle) >= 100 and (ChangeInArticle*PastChangeInSize) < 0:
                            yAxis.pop()
                            xAxis.pop()
                            count -= 1
                            error = ChangeInArticle
                            print('Revert Found!')
        
                        else:
                            yAxis.append(ChangeInArticle)
                            count += 1
                            xAxis.append(count)
                            if PastChangeInSize > MaxChange and error != PastChangeInSize:
                                MaxChange = PastChangeInSize
                                MaxChangeDate = Pastdate
        							#print(ChangeInArticle, count, SizeOfArticle, PastChangeInSize,'\n','\n')
        
        					#print(ChangeInArticle, count, SizeOfArticle, PastChangeInSize)
                        previousSize = SizeOfArticle
                        PastChangeInSize = ChangeInArticle
                        Pastdate = dateTemp
    					
    
    	#print(MaxChangeDate, MaxChange, articleName, FeaturedDate)
    plt.plot(xAxis, yAxis, 'r-')
    plt.xlabel('Number of Intervals')
    plt.ylabel('Change in Bytes')
    plt.title('Change in size over time of ' + articleName)
    plt.savefig('change_in_bytes_plot/plot'+str(num)+'.png',dpi=800)


    plt.show()
    
def main():
    num = 1
    for i,j in zip(featuredArticleList1,featuredArticleList2): #For each featured article get the starting time
        FeaturedDate = GetFeaturedArticleDate(i)
        PlotChangeInSizeGraph(j, FeaturedDate,num)
        num+=1			
    
main()
