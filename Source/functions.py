from nltk.tag import pos_tag
import matplotlib.pyplot as plt
from nltk import word_tokenize
from nltk import sent_tokenize
import copy
import string
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import re #for matching expressions
import time #for delaing with broken connection to web.
import requests #for connection to web.
import os

class TrieNode:

    def __init__(self):
        self.children = {}
        self.isEndOfWord = False;

class Trie:

    def __init__(self):
        self.root  = TrieNode();

    def getChild(self,trieNode,word):
        if(word in trieNode.children.keys()):
            return trieNode.children[word];
        else:
            trieNode.children[word] = TrieNode();
            return trieNode.children[word];

    def checkWord(self,trieNode,word):
        if(word in trieNode.children.keys()):
            return trieNode.children[word];
        else:
            return None;


    def insert(self,key):
        key = key.lower()
        tempTrieNode = self.root;
        for i in key:
            tempTrieNode = self.getChild(tempTrieNode,i);
        tempTrieNode.isEndOfWord = True

    def search(self,key):
        key=key.lower()
        tempTrieNode = self.root;
        for i in key:
            tempTrieNode = self.checkWord(tempTrieNode,i);
            if(tempTrieNode==None):
                return False;
        if(tempTrieNode.isEndOfWord == False):
            return False;
        return True;




def graphWords(text,averageOverWords=100,tags=["NNP","NNPS"],title="graph"):
    #Tokanize the text if it is not already tokenized and find the tags of each word.
    if(type(text) == str):
        tagged_sent =  pos_tag(word_tokenize(text))
    else:
        tagged_sent = pos_tag(text)
    #stores  wordCount for every "averageOverWords" words  
    Xaxis = []
    #stores  newNounCount for every "averageOverWords" words
    Yaxis = [] 
    
    Y1axis = []
    # stores all collected nouns
    collectedWords = []
    #Stores current Word Count 
    wordCount = 0 
    #Stores current new noun Count
    newNounCount = 0 
    #Stores current noun count
    nounCount = 0

    for tagged_word in tagged_sent:
        if hasNumbers(tagged_word[0]) == False and hasPunctuations(tagged_word[0]) == False and len(tagged_word[0]) > 1:  #to remove words like ",","132" etc.
            wordCount+=1 
            if(tagged_word[1] in tags):
                nounCount+=1
                if(tagged_word[0] not in collectedWords):
                    newNounCount+=1
                    collectedWords+=[tagged_word[0]]
            if(wordCount%averageOverWords == 0):
                Xaxis+=[wordCount]
                Yaxis+=[newNounCount]
                Y1axis+=[nounCount]
    Xaxis += [wordCount]
    Yaxis += [newNounCount]
    Y1axis += [nounCount]
    #Y2axis =copy.deepcopy(Y1axis) 
    excpectedCouponCount(Y1axis,newNounCount)
    plt.xlabel('Words Count')
    plt.ylabel(" Noun Count")
    plt.plot(Xaxis,Yaxis)
    plt.plot(Xaxis,Y1axis,"r")
    plt.savefig(title+".png")
    plt.close()

"""probabilitiesOfCoupons:  
    input: n (int) : total number of coupons
           tries(int) : maximum number of tries
    output:an matrix (tries * n)
            description of matrix : matrix[i][j] means probability of getting j new coupons in i+1 trie

"""
def probabilitiesOfCoupons(n,tries):
    probabilities = [[0.0 for i in range(j+1)] for j in range(tries)];
    probabilities[0][0]=1.0
    for i in range(1,tries):
        for j in range(i+1):
            #keeping check on corner cases
            if(j==n-1):
                probabilities[i][j] = probabilities[i-1][j-1]*((n-j)/n);
                if(len(probabilities[i-1]) >= n ):
                    probabilities[i][j] +=probabilities[i-1][j]*((j+1)/n);
                break;
            if(j == 0):
                probabilities[i][j] = probabilities[i-1][j]*(1/n);
            elif(j == i):
                probabilities[i][j] = probabilities[i-1][j-1]*((n-j)/n);
            else:
                #probability of getting j new coupons in i+1 th trie is:
                #probability of not getting any new coupon in i+1 th try * probability of getting j new coupons in i-1 th try + probability of getting new coupon in i+1th try * probability of getting j-1 new coupons in ith try 
                probabilities[i][j] = probabilities[i-1][j-1]*((n-j)/n) + probabilities[i-1][j]*((j+1)/n);
    return probabilities
def excpectedCouponCount(Y1axis,n):
    m = len(Y1axis);
    probabilities = probabilitiesOfCoupons(n,Y1axis[m-1])
    for i in range(m):
        tries = Y1axis[i]
        excpectedCoupons = 0;
        for j in range(tries):
            excpectedCoupons += probabilities[tries-1][j]*(j+1)
        Y1axis[i]=excpectedCoupons

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def hasPunctuations(inputString):
    invalidChars = set(string.punctuation)
    if any(char in invalidChars for char in inputString):
        return True
    else:
        return False

def getNewNounsCount(text,trie,tags = ["NNP","NNPS"]):
    numberOfNouns = 0
    words =  word_tokenize(text) #get every word in the text
    for tagged_word in words: #for every word in the text
        #if the word is new word
        if(trie.search(tagged_word) == False):
            #if it is not number or punctuations or a single letter
            if hasNumbers(tagged_word) == False and hasPunctuations(tagged_word) == False and len(tagged_word) > 1:
                #if it is a noun
                if pos_tag([tagged_word])[0][1] in tags :
                	numberOfNouns +=1
            trie.insert(tagged_word[0]);
    return numberOfNouns 
 
def graphWikiPerDay(title):
    pageTitle = title
    url="https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvprop=timestamp|content&rvlimit=max&rvdir=newer&titles="+pageTitle   #url for getting data
    tags = ["NNP","NNPS"]
    next = ""                                             #information for the next request
    
    fmt = "%Y-%m-%dT%H:%M:%SZ"

    #initial starting Date 
    d1 = datetime.strptime("2001-1-1T0:0:0Z",fmt);
    firsTime = True;
    myset = set()
    nounCount = 0;
    XY={}
    cleanr = re.compile('<.*?>')
    count = 0;
    X=[]
    while True:
        response=""
        #Getting the request page
        while(response==""):
            try:
                response = requests.get(url + next)  #web request
                if (response.content==""):
                    response=""
            except:
                print ("sleeping started")
                time.sleep(5)     
                print("sleeping ended")
        
        #parsing the xml file.
        e =  ET.fromstring(response.content);
        start = time.clock()
        #for every revesion in the page
        for rev in e.find('query').find('pages').find('page').find('revisions').findall('rev'):
            if(firsTime == False):
                d1 = datetime.strptime(rev.get("timestamp"),fmt);
                firsTime == False
            wikiText =  (re.sub(cleanr,"",str(rev.text)))
            tagged_words = pos_tag(word_tokenize(wikiText))
            for tagged_word in tagged_words:
                if hasNumbers(tagged_word[0]) == False and hasPunctuations(tagged_word[0]) == False and len(tagged_word[0]) > 1:  #to remove words like ",","132" etc.
                    if(tagged_word[1] in tags):
                        if(tagged_word[0] not in myset):
                            nounCount+=1
                            myset.add(tagged_word[0]);
            d2 = datetime.strptime(rev.get("timestamp"),fmt);
            X.append((d2-d1).days)
            XY[(d2-d1).days] = nounCount
        count=count+1
        tempv = e.find('continue')
        if not tempv:                                      #break the loop if 'continue' element missing
            break
        cont = tempv.get('rvcontinue')
        print(str(count)+" page Completed : " + str(time.clock()-start)+ "ms"+ "rvcontinue = "+ cont);

        next = "&rvcontinue=" + str(cont)            #gets the revision Id from which to start the next request
    lists = sorted(XY.items())
    x, y = zip(*lists);
    plt.plot(x, y,label='original_graph');
    Y=[i for i in X]
    excpectedCouponCount(Y,nounCount)
    plt.plot(X,Y,label='Coupon_Collector_Graph(n= '+str(nounCount)+')');
    plt.savefig(str(title)+"_date.png");
    plt.show();


def graphWikiPerRevision(title):
    pageTitle = title
    url="https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvprop=content&rvlimit=max&rvdir=newer&titles="+pageTitle   #url for getting data
    tags = ["NNP","NNPS"]
    next = ""                                             #information for the next request
    firsTime = True
    #initial starting Date 
    myset = set()
    nounCount = 0;
    XY=[]
    cleanr = re.compile('<.*?>')
    count = 0;
    X=[]
    while True:
        response=""
        #Getting the request page
        while(response==""):
            try:
                response = requests.get(url + next)  #web request
                if (response.content==""):
                    response=""
            except:
                print ("sleeping started")
                time.sleep(5)     
                print("sleeping ended")
        
        #parsing the xml file.
        e =  ET.fromstring(response.content);
        start = time.clock()
        #for every revesion in the page

        for rev in e.find('query').find('pages').find('page').find('revisions').findall('rev'):
            if(firsTime == False):
                d1 = datetime.strptime(rev.get("timestamp"),fmt);
                firsTime == False
            wikiText =  (re.sub(cleanr,"",str(rev.text)))
            tagged_words = pos_tag(word_tokenize(wikiText))
            for tagged_word in tagged_words:
                if hasNumbers(tagged_word[0]) == False and hasPunctuations(tagged_word[0]) == False and len(tagged_word[0]) > 1:  #to remove words like ",","132" etc.
                    if(tagged_word[1] in tags):
                        if(tagged_word[0] not in myset):
                            nounCount+=1
                            myset.add(tagged_word[0]);
            XY.append(nounCount)
        tempv = e.find('continue')
        if tempv == None:                                      #break the loop if 'continue' element missing
            break
        cont = tempv.get('rvcontinue')
        count +=1
        print(str(count)+" page Completed : " + str(time.clock()-start)+ "ms "+ "rvcontinue = "+ cont);
        next = "&rvcontinue=" + str(cont)            #gets the revision Id from which to start the next request
    plt.plot(XY,label='original_graph');
    X = [i for i in range(len(XY))]
    plt.xlabel('number of revisions---------->');
    plt.ylabel('cummulative newNounCount count ---------------->');
    excpectedCouponCount(X,nounCount)
    plt.plot(X,label='Coupon_Collector_Graph(n= '+str(nounCount)+')');
    plt.legend()
    plt.savefig(str(title)+"_rev.png");
    plt.show();


def getFirstRev(path):
	tree = ET.parse(path)
	root = tree.getroot()
	return list(root.iter('{http://www.mediawiki.org/xml/export-0.10/}text'))[0].text
		



def getRefData(path,getfirstrev=getFirstRev):
	Refdict={}
	myset = set()
	content = getfirstrev(path)
	refTags = re.findall(r'<ref.*?>.*?/ref>',content);
	for tag in refTags:
		urls = re.findall(r"http://[^ ]*",tag);
		for url in urls:
			if url not in myset:
				domain = re.findall(r"http://[^/]*",url)
				if domain[0] in Refdict.keys():
					Refdict[domain[0]] += 1
				else:
					Refdict[domain[0]] = 1
				myset.add(url)
	return Refdict

def getRatio(path):
	Refdict = {}
	filesList = os.listdir(path);
	n = len(filesList)
	numOfRev = 0
	for i in range(n):
		filename = filesList[i]
		tree = ET.parse(os.path.join(path,filename));
		root = tree.getroot();
		for rev in root.find('{http://www.mediawiki.org/xml/export-0.10/}page').findall('{http://www.mediawiki.org/xml/export-0.10/}revision'):
			numOfRev+=1
			revText = rev.find('{http://www.mediawiki.org/xml/export-0.10/}text').text;
			refTags = re.findall(r'<ref.*?>.*?/ref>',revText);
			myset = set()
			for tag in refTags:
				urls = re.findall(r"http://[^ |]*",tag)
				if len(urls)!=0:
					url = urls[0]
					if url not in myset:
						if url not in Refdict:
							Refdict[url] = 1;
						else:
							Refdict[url] +=1;
						myset.add(url);
	#finding average
	su=0
	ma = 0
	for ref in Refdict:
		su+=Refdict[ref];
		if(ma<Refdict[ref]):
			ma = Refdict[ref] 
	avg = su/len(Refdict);
	print("Total Number Of Revisions : "+str(numOfRev))
	print("highest age of a Reference : "+str(ma)+" revisions")
	print("Avg age of a Ref : "+str(avg)+" revisions")
	numberOfRelaibleRev = 0
	for lrev in myset:
		if Refdict[lrev]>=avg:
			numberOfRelaibleRev+=1
	print("No of relaible Reference in latest revision : "+str(numberOfRelaibleRev)+ " revisions")
	print("Total no of revisions in latest revision : "+str(len(myset))+ " revisions")
	ratio = numberOfRelaibleRev/len(myset)
	print("ratio : "+str(ratio))
	return ratio

def getRatioOnFlyByRev(title):
    numOfRev=0
    pageTitle = title
    Refdict = {}
    urlOfTitle="https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvprop=content&rvlimit=max&rvdir=newer&titles="+pageTitle   #url for getting data
    next = ""                                             #information for the next request
    cleanr = re.compile('<.*?>')
    count = 0;
    while True:
        response=""
        #Getting the request page
        while(response==""):
            try:
                response = requests.get(urlOfTitle + next)  #web request
                if (response.content==""):
                    response=""
            except:
                print ("sleeping started")
                time.sleep(5)     
                print("sleeping ended")
        
        #parsing the xml file.
        e =  ET.fromstring(response.content);
        start = time.clock()
        #for every revesion in the page

        for rev in e.find('query').find('pages').find('page').find('revisions').findall('rev'):
            numOfRev+=1
            revText = rev.text;
            refTags = re.findall(r'<ref.*?>.*?/ref>',revText);
            myset = set()
            for tag in refTags:
                urls = re.findall(r"http://[^ |]*",tag)
                if len(urls)!=0:
                    url = urls[0]
                    if url not in myset:
                        if url not in Refdict:
                            Refdict[url] = 1;
                        else:
                            Refdict[url] +=1;
                        myset.add(url);
        tempv = e.find('continue')
        if tempv == None:                                      #break the loop if 'continue' element missing
            break
        cont = tempv.get('rvcontinue')
        print(str(count)+" page Completed : " + str(time.clock()-start)+ "ms "+ "rvcontinue = "+ cont);
        next = "&rvcontinue=" + str(cont)            #gets the revision Id from which to start the next request
    su=0
    ma = 0
    for ref in Refdict:
        su+=Refdict[ref];
        if(ma<Refdict[ref]):
            ma = Refdict[ref] 
    avg = su/len(Refdict);
    print("Total Number Of Revisions : "+str(numOfRev))
    print("highest age of a Reference : "+str(ma)+" revisions")
    print("Avg age of a Ref : "+str(avg)+" revisions")
    numberOfRelaibleRev = 0
    for lrev in myset:
        if Refdict[lrev]>=avg:
            numberOfRelaibleRev+=1
    print("No of relaible Reference in latest revision : "+str(numberOfRelaibleRev)+ " revisions")
    print("Total no of revisions in latest revision : "+str(len(myset))+ " revisions")
    ratio = numberOfRelaibleRev/len(myset)
    print("ratio : "+str(ratio))
    return ratio

def getRatioOnFlyByDate(title):
    numOfRev=0
    pageTitle = title
    Refdict = {}
    urlOfTitle="https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvprop=timestamp|content&rvlimit=max&rvdir=newer&titles="+pageTitle   #url for getting data
    next = ""                                             #information for the next request
    cleanr = re.compile('<.*?>')
    count = 0;
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    while True:
        response=""
        #Getting the request page
        while(response==""):
            try:
                response = requests.get(urlOfTitle + next)  #web request
                if (response.content==""):
                    response=""
            except:
                print ("sleeping started")
                time.sleep(5)     
                print("sleeping ended")
        
        #parsing the xml file.
        e =  ET.fromstring(response.content);
        start = time.clock()
        #for every revesion in the page

        for rev in e.find('query').find('pages').find('page').find('revisions').findall('rev'):
            numOfRev+=1
            revText = rev.text;
            if revText == None:
                continue
            refTags = re.findall(r'<ref.*?>.*?/ref>',revText);
            myset = set()
            for tag in refTags:
                urls = re.findall(r"http://[^ |]*",tag)
                if len(urls)!=0:
                    url = urls[0]
                    if url not in myset:
                        if url not in Refdict:
                            Refdict[url] =[datetime.strptime(rev.get("timestamp"),fmt),datetime.strptime(rev.get("timestamp"),fmt)];
                        else:
                            Refdict[url][1]=datetime.strptime(rev.get("timestamp"),fmt);
                        myset.add(url);
        tempv = e.find('continue')
        if tempv == None:                                      #break the loop if 'continue' element missing
            break
        cont = tempv.get('rvcontinue')
        count +=1
        print(str(count)+" page Completed : " + str(time.clock()-start)+ "s "+ "rvcontinue = "+ cont);
        next = "&rvcontinue=" + str(cont)            #gets the revision Id from which to start the next request
    su=0
    ma = 0
    for lrev in myset:
        Refdict[lrev][1] = datetime.now()
    for ref in Refdict:
        su+=(Refdict[ref][1]-Refdict[ref][0]).days;
        if(ma<(Refdict[ref][1]-Refdict[ref][0]).days):
            ma = (Refdict[ref][1]-Refdict[ref][0]).days 
    avg = su/len(Refdict);
    ratio = 0
    with open(title+"_Date.report",'w') as f:
        f.write("Total Number Of Revisions : "+str(numOfRev))
        f.write("\n")
        f.write("highest age of a Reference : "+str(ma)+" days\n")
        f.write("Avg age of a Ref : "+str(avg)+" days\n")
        numberOfRelaibleRev = 0
        for lrev in myset:
            print(Refdict[lrev])
            if (Refdict[lrev][1]-Refdict[lrev][0]).days>=avg:
                numberOfRelaibleRev+=1
        f.write("No of relaible Reference in latest revision : "+str(numberOfRelaibleRev)+ " revisions\n")
        f.write("Total no of revisions in latest revision : "+str(len(myset))+ " revisions\n")
        ratio = numberOfRelaibleRev/len(myset)
        f.write("ratio : "+str(ratio))
        f.write("\n")
    return ratio


def vaibhav(path):
    tree = ET.parse(path);root = tree.getroot();
    root = tree.getroot();
    fil = open(path+"1","w");
    for rev in root.find('{http://www.mediawiki.org/xml/export-0.10/}page').findall('{http://www.mediawiki.org/xml/export-0.10/}revision'):
        text = rev.find('{http://www.mediawiki.org/xml/export-0.10/}text').text;
        tags=["NNP","NNPS"]
        tagged_sent =  pos_tag(word_tokenize(text))
        fil.write("TimeStamp:"+rev.find("{http://www.mediawiki.org/xml/export-0.10/}timestamp").text+"\n");
        for tagged_word in tagged_sent:
            if hasNumbers(tagged_word[0]) == False and hasPunctuations(tagged_word[0]) == False and len(tagged_word[0]) > 1:  #to remove words like ",","132" etc.
                if(tagged_word[1] in tags):
                    fil.write(tagged_word[0]+" , ")
        print("one revision completed!!")
        fil.write("\n=====================================================================\n")

