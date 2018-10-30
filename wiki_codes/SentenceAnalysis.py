#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 15:42:53 2018

@author: descentis
"""

import xml.etree.cElementTree as ec
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
import mwparserfromhell

def sentenceAnalysis(articleName):
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
    wikicode = str(wikicode)                        
    sentence_list = sent_tokenize(wikicode)
    
    final_sent = []
    for sent in sentence_list:
        start = -1
        end = -1
        for i in range(len(sent)):
            if(sent[i]=='<' and sent[i+1]=='r'):
                start = i
            if(sent[i]=='<' and sent[i+1]=='/' and sent[i+2]=='r'):
                end = i+5
                  
        
        new_sent = sent[:start]+sent[end+1:]
        final_sent.append(new_sent)
                

    for i in final_sent:
        print(i)
        print("******")
sentenceAnalysis('Indian Institute of Technology Ropar.xml')