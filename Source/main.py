import nltk
import os
from functions import *
import sys

# -*- coding: utf-8 -*-

exp = int(sys.argv[1])

if(exp == 1):
    #fields contains names of every fiction article in nltk.corpus.gutenberg.  
    fields = nltk.corpus.gutenberg.fileids()

    #for every fiction article:
    #plot the graph and save it as fieldName.png
    os.chdir("../Data")
    if not os.path.exists("Gutenberg_Graphs"):
        os.makedirs("Gutenberg_Graphs")
    os.chdir("Gutenberg_Graphs")
    for field in fields:
        graphWords(nltk.corpus.gutenberg.words(field) , title=str(field))
        print ("saved " + str(field) +".png")
        break

elif(exp == 2):
    graphWikiPerRevision(sys.argv[2]);

elif(exp == 6):
    graphWikiPerDay(sys.argv[2]);

elif(exp == 3):
    pageTitle = sys.argv[2]
    url="https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&rvprop=timestamp|content&rvlimit=max&rvdir=newer&titles="+pageTitle
    next = "" #information for the next request
    
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
        print("got page requested..");
        path = os.path.join("..","Data","Exp3",pageTitle+".txt");
        fil = open(path,"w");
        for rev in e.find('query').find('pages').find('page').find('revisions').findall('rev'):
            text = re.sub(cleanr,"",str(rev.text))
            tags=["NNP","NNPS"]
            tagged_sent =  pos_tag(word_tokenize(text))
            fil.write("TimeStamp:"+rev.get("timestamp")+"\n");
            for tagged_word in tagged_sent:
                if hasNumbers(tagged_word[0]) == False and hasPunctuations(tagged_word[0]) == False and len(tagged_word[0]) > 1:  #to remove words like ",","132" etc.
                    if(tagged_word[1] in tags):
                        fil.write(tagged_word[0]+" , ")
            print("one revision completed!!")
            fil.write("\n=====================================================================\n")

elif(exp == 4):
    getRatioOnFlyByDate(sys.argv[2]);

elif(exp == 5):
	vaibhav(sys.argv[2])

elif(exp == 7):
    os.chdir("../Data")
    if not os.path.exists("Reports"):
        os.makedirs("Reports")
    os.chdir("Reports");
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])
    os.chdir(sys.argv[2])
    graphWikiPerRevision(sys.argv[2]);
    getRatioOnFlyByDate(sys.argv[2])

elif(exp == 8):
    os.chdir("../Data")
    if not os.path.exists("Reports"):
        os.makedirs("Reports")
    ratioDict= {}
    file = open(os.path.join(".","Reports",sys.argv[2]+".report"),"w");
    with open(sys.argv[2],"r") as f:
        for articlei in f:
            article = articlei.strip()
            print(article.encode(encoding='utf-8'))
            ratioDict[article]=getRatioOnFlyByDate(article);
            file.write(str(article)+" : "+str(ratioDict[article]))
            file.write("\n")
    file.close();
    """for key in ratioDict:
        if(ratioDict[key]>0):
            avg += ratioDict[key]
        else:
            numUnRel+=1
    avg = avg/(len(ratioDict)-numUnRel)
    os.chdir("Reports");
    with open(str(sys.argv[2])+".report","w") as fi:
        fi.write("total number of articles : "+ str(len(ratioDict)))
        fi.write("\n")
        fi.write("average ratio of articles : "+str(avg))
        fi.write("\n")
        fi.write("unrelaible articles : "+str(numUnRel))
        fi.write("\narticles above average:\n")
        for key in ratioDict:
            if(ratioDict[key]>=avg):
                fi.write(str(key)+" : "+str(ratioDict[key]))
                fi.write("\n")
        fi.write("articles below average : \n")
        for key in ratioDict:
            if(ratioDict[key]<avg and ratioDict[key] != -1 and ratioDict[key] != -2):
                fi.write(str(key)+" : "+str(ratioDict[key]))
                fi.write("\n")
        fi.write("unrelaible articles : \n")
        for key in ratioDict:
            if(ratioDict[key]==-1):
                fi.write(str(key)+" : "+str(ratioDict[key]))
                fi.write("\n")"""
elif(exp == 9):
    os.chdir("../Data")
    if not os.path.exists("Graphs"):
        os.makedirs("Graphs")
    os.chdir("Graphs")
    with open(sys.argv[2],"r") as f:
        for articlei in f:
            article = articlei.strip()
            print(article.encode(encoding='utf-8'))
            graphWikiPerRevision(article);

