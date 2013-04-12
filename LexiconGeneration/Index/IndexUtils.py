import lucene
import nltk
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, IndexSearcher, Version, QueryParser
import os, sys, re

from LexiconGeneration import  Parsed_Item





def searchOne(line,searcher,analyzer, replace):
    'returns array of sentences in new data type'
    #print "line: "+line
    string = clean_stringTest(line, replace)
    query = QueryParser(Version.LUCENE_35, "title", analyzer).parse(string)
    MAX = 1
    hits = searcher.search(query, MAX)
    result_list = []
    try:
        hm_tmp = {}
        for hit in hits.scoreDocs:
            doc = searcher.doc(hit.doc)
            #sentence1 = doc.get("title").encode("utf-8")
            sentence1 = doc.get("title").encode("utf-8")
            #print "returned sentence: "+sentence1
            hm_tmp[sentence1] = ""
        for key in hm_tmp:
            sentence_tmp = sentence_wrapper(key)
            result_list.append(sentence_tmp)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        print "in Index Util in getting the documents from lucene and converting them to the new data type\n\n"
        #raw_input("wait")
        
    return result_list

def searchWithoutWrapper(line,searcher,analyzer, replace):
    'returns array of sentences in new data type'
    #print "line: "+line
    string = clean_stringTest(line, replace)
    query = QueryParser(Version.LUCENE_35, "title", analyzer).parse(string)
    MAX = 1
    hits = searcher.search(query, MAX)
    result_list = []
    try:
        hm_tmp = {}
        for hit in hits.scoreDocs:
            doc = searcher.doc(hit.doc)
            #sentence1 = doc.get("title").encode("utf-8")
            sentence1 = doc.get("title").encode("utf-8")
            result_list.append(sentence1)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        print "in Index Util in getting the documents from lucene and converting them to the new data type\n\n"
        raw_input("wait")
        
    return result_list


def clean_string(string):
    replace = str.replace
    if string.startswith(" "):
        string = string[1:]
    array = re.findall(r'[\w\s]+',string)
    string = ""
    for item in array:
        string+=item
    string = replace(string.lower(),"not","")
    string = replace(string.lower(),"or","")
    string = replace(string.lower(),"and","")
    while "  " in string:
        string = replace(string,"  ", " ")
    string = replace(string,"  "," ")
    string = replace(string," ", " AND ")
    string = replace(string,"AND  AND","AND")
    if string.startswith(" AND "):
        string = string[5:]
    if string.endswith(" "):
        string = string[:-1]
    if string.endswith("AND"):
        string = string[:-3]
    #raw_input(string)
    return string
    

def clean_stringTest(string,replace):
    #TODO: Check after paper, why this does not work!!!!
    
    #print "in clean stringTest"
    #return clean_string(string)

    if string[0:1] == " ":
        string = string[1:]
    string = replace(string,"-", "")
    string = replace(string,"(", "")
    string = replace(string,")", "")
    string = replace(string,"_", "")
    string = replace(string,"&#39;", "")
    string = replace(string,"&quot;", "")
    string = replace(string,":", "")
    string = replace(string,"!", "")
    string = replace(string,".", "")
    string = replace(string,":", "")
    string = replace(string,"+", "")
    string = replace(string,"-", "")
    string = replace(string,",", "")
    string = replace(string,"|", "")
    string = replace(string,"\"","")
    string = replace(string,"[","")
    string = replace(string,"]","")
    string = replace(string,"^","")
    string = replace(string,"}","")
    string = replace(string,"{","")
    string = replace(string,"=","")
    string = replace(string,"/","")
    string = replace(string,".", "") #string=string.replace("  ", "");
    while "  " in string:
        string = replace(string,"  ", " ")
    
    string = replace(string,"~", "")
    string = replace(string,"*", "")
    string = replace(string,"?", "")
    
    #TODO: the following three lines create an error....
    #string = replace(string.lower(),"not","")
    #string = replace(string.lower(),"or","")
    #string = replace(string.lower(),"and","")
    
    string = replace(string," ", " AND ")
    
    if string.startswith(" AND "):
        string = string[5:]
    if string.endswith(" "):
        string = string[:-1]
    if string.startswith(" "):
        string = string[1:]
    if string.endswith("AND"):
        string = string[:-3]
    return string
    

def does_line_exist(line, searcher, analyzer, replace):
    hits = None
    try:
        query_string = clean_stringTest(line, replace)
        query = QueryParser(Version.LUCENE_35, "title", analyzer).parse(query_string)
        MAX = 10
        hits = searcher.search(query, MAX)
    except Exception:
        #print "Unexpected error in does line exists in Index Utils:", sys.exc_info()[0]
        #print "query_string: "+"START"+query_string+"DONE"
        #print 
        #print
        return None
    if len(hits.scoreDocs)>0:
        return True
    else:
        return False
    
    
def tokenize(string):
        'tokenizes a sentence and returns token'
        return nltk.word_tokenize(string)
    
def sentence_wrapper(sentence):
    array = []
    if "  " in sentence:
        working_array = sentence.split("  ")
        for item in working_array:
            if " " in item:
                pArray = item.split(" ")
                pItem = Parsed_Item.ParsedItem(pArray[0],pArray[1],pArray[2],pArray[3],pArray[4],pArray[5],pArray[6],pArray[7],pArray[8], pArray[9])
                array.append(pItem)
    return array

def getItemAtr(item):
    return item.__getattr__("pos0")+" "+item.__getattr__("pos1")+" "+item.__getattr__("pos2")+" "+item.__getattr__("pos3")+" "+item.__getattr__("pos4")+" "+item.__getattr__("pos5")+" "+item.__getattr__("pos6")+" "+item.__getattr__("pos7")+" "+item.__getattr__("pos8")+" "+item.__getattr__("pos9")+"  "


def reverse_sentence_wrapper(sentence_array):
    
    slist = [getItemAtr(item) for item in sentence_array]
    sentence = "".join(slist)
    sentence = sentence[:len(sentence)-2]
    return sentence
