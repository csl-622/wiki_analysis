import nltk
import os
from functions import *
import sys



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

elif(exp == 2):
    graphWiki(sys.argv[2]);

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


