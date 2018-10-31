import nltk
import os
from functions import *
import sys
from getData import *



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

