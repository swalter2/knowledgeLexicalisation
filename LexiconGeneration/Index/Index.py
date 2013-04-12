#Used PyLucene Implementation: http://www.apache.org/dist/lucene/pylucene/pylucene-3.6.0-2-src.tar.gz

import lucene
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, IndexSearcher, Version, QueryParser
#import IndexUtils
#from time import time
import re

class LuceneIndex():
    analyzer = None
    searcher = None
    replace = None
    
    def __init__(self, path_to_index):
        global analyzer
        global searcher
        
        lucene.initVM()
        index_dir = SimpleFSDirectory(File(path_to_index))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        searcher = IndexSearcher(index_dir)
        global replace
        replace = str.replace
    

    def clean_string(self, string):
        if string.startswith(" "):
            string = string[1:]
        array = re.findall(r'[\w\s]+',string)
        string = ""
        for item in array:
            string+=item

#        string = replace(string.lower(),"not","")
#        string = replace(string.lower(),"or","")
#        string = replace(string.lower(),"and","")
        
        
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

    def search(self, string , rank):
        #t1 = time()
        
        #string = self.clean_string(string)
        #print "LuceneString "+string
        
        try:
            #query = QueryParser(Version.LUCENE_35, "title", analyzer).parse(string)
            MAX = 100000
            
            array = re.findall(r'[\w\s]+',string)
            string = ""
            for item in array:
                string+=item
            qp = QueryParser(Version.LUCENE_35, "title", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(string)
                        
            hits = searcher.search(query, MAX)
    
            #print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
            
            sentence_list = []
            for hit in hits.scoreDocs:
                #if hit.score > 0:
                doc = searcher.doc(hit.doc)
                sentence_list.append(doc.get("title").encode("utf-8"))
            return sentence_list
        except:
            print("Fail in receiving sentence with term "+string)
    
#    def index(self):
#        'indexes files, in the moment specified to '
#        lucene.initVM()
#        indexDir = "/windows/C/JulyLuceneIndex2"
#        dir = SimpleFSDirectory(File(indexDir))
#        analyzer = StandardAnalyzer(Version.LUCENE_35)
#        writer = IndexWriter(dir, analyzer, True, IndexWriter.MaxFieldLength(512))
#        file_name = "/windows/C/WikipediaDump/tmpwiki.tmp"
#            
#            
#        f = open(file_name,"r")
#        #hm={}
#        #for line in f:
#        #    line=line.replace("\n","")
#        #    hm[line]=""
#        # 
#        anzahl=0
#        for line in f:
#            anzahl+=1
#            line = line.replace("\n","")
#            if anzahl%10000==0:
#                print anzahl
#            doc = Document()
#            doc.add(Field("title", line, Field.Store.YES, Field.Index.ANALYZED))
#            writer.addDocument(doc)
#        writer.close() 
#        f.close()
#        
#        print anzahl
#        print "done"

    
        
