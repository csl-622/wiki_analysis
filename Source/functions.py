from nltk.tag import pos_tag
#import matplotlib.pyplot as plt
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
				#probability of getting j new coupons in i+1 th try is:
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
 
def graphWiki(title):
    pageTitle = title
    url="https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvprop=timestamp|content&rvlimit=max&rvdir=newer&titles="+pageTitle   #url for getting data
    tags = ["NNP","NNPS"]
    next = ""                                             #information for the next request
    
    fmt = "%Y-%m-%dT%H:%M:%SZ"

    #initial starting Date 
    d1 = datetime.strptime("2001-1-1T0:0:0Z",fmt);
    firsTime = True;
    trie = Trie()
    nounCount = 0;
    XY={}
    cleanr = re.compile('<.*?>')
    count = 0;
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
            if(firsTime):
                d1 = datetime.strptime(rev.get("timestamp"),fmt);
                firsTime == False
            wikiText =  (re.sub(cleanr,"",str(rev.text)))
            print (wikiText)
            tagged_words = pos_tag(word_tokenize(wikiText))
            for tagged_word in tagged_words:
                if hasNumbers(tagged_word[0]) == False and hasPunctuations(tagged_word[0]) == False and len(tagged_word[0]) > 1:  #to remove words like ",","132" etc.
                    if(tagged_word[1] in tags):
                    	if(trie.search(tagged_word[0])):
                    		nounCount+=1
                    		trie.insert(tagged_word[0]);
            d2 = datetime.strptime(rev.get("timestamp"),fmt);
            XY[(d2-d1).days] = nounCount
        count=count+1
        cont = e.find('continue').get('rvcontinue')
        print(str(count)+" page Completed : " + str(time.clock()-start)+ "ms"+ "rvcontinue = "+ cont);
        if not cont:                                      #break the loop if 'continue' element missing
            break

        next = "&rvcontinue=" + str(cont)            #gets the revision Id from which to start the next request
    lists = sorted(d.items())
    x, y = zip(*lists);
    plt.plot(x, y);
    plt.savefig("test.png");
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
