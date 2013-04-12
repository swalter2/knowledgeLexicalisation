#Used PyLucene Implementation: http://www.apache.org/dist/lucene/pylucene/pylucene-3.6.0-2-src.tar.gz

import lucene
from lucene import \
SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, IndexSearcher, Version, QueryParser
#import IndexUtils
#from time import time
import re, glob


#####################################
#####################################
##
## anchor
## anchor_uri 
## dbpedia_uri
## number
##
##
##
#####################################
#####################################

class LuceneIndex():
    analyzer = None
    searcher = None
    replace = None
    
    def __init__(self, path_to_index):
        global analyzer
        global searcher
        
        lucene.initVM()
        #self.index(path_to_index, path_files)
        dir = SimpleFSDirectory(File(path_to_index))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        searcher = IndexSearcher(dir)
        global replace
        replace = str.replace
       
    

    def clean_string(self, string):
        if string.startswith(" "):
            string = string[1:]
        array = re.findall(r'[\w\s]+',string)
        string = ""
        for item in array:
            string+=item

        
        
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

    def searchForAnchor(self, string):

        string = self.clean_string(string)
        
        #string = string.replace("AND","OR")

       # print "search term: "+string
        try:
            query = QueryParser(Version.LUCENE_35, "anchor", analyzer).parse(string)
            MAX = 10000
            #print "Query: "+str(query)
            result = []
            hits = searcher.search(query, MAX)
            #print len(hits.scoreDocs)
            for hit in hits.scoreDocs:
                #print str(hit.score)
                #if hit.score > 2:
                doc = searcher.doc(hit.doc)
                result.append([doc.get("anchor").encode("utf-8"), doc.get("anchor_uri").encode("utf-8"), doc.get("dbpedia_uri").encode("utf-8"), doc.get("number").encode("utf-8")])
            return result
        except:
            print("Fail in "+string)
            return []
            
    def searchExactAnchor(self, string):
        string_old = string
        string = self.clean_string(string)
        try:
            query = QueryParser(Version.LUCENE_35, "anchor", analyzer).parse(string)
            MAX = 10000
            result = []
            hits = searcher.search(query, MAX)
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                anchor = doc.get("anchor").encode("utf-8")
                if anchor.lower() == string_old.lower():
                    result.append([anchor, doc.get("anchor_uri").encode("utf-8"), doc.get("dbpedia_uri").encode("utf-8"), doc.get("number").encode("utf-8")])
            return result
        except:
            print("Fail in "+string)
            return []
            
            
    def searchForDbpediaURI(self, uri):
        uri_old = uri
        uri = uri.replace("http://dbpedia.org/resource/","")

        array = re.findall(r'[\w\s]+',uri)
        uri = ""
        for item in array:
            uri+=item
        
        try:
            #query = QueryParser(Version.LUCENE_35, "dbpedia_uri", analyzer).parse(uri)
            qp = QueryParser(Version.LUCENE_35, "dbpedia_uri", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(uri)
            MAX = 10000
            result = []
            hits = searcher.search(query, MAX)
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                dbpedia_uri = doc["dbpedia_uri"].encode("utf-8")
                if dbpedia_uri == uri_old:
                    result.append([doc["anchor"].encode("utf-8"), doc["anchor_uri"].encode("utf-8"), dbpedia_uri, doc["number"].encode("utf-8")])
            return result
        except:
            print("Fail in uri: "+uri)
            return []
            
    def searchForDbpediaURIreturnAnchor(self, uri):

        uri = uri.replace("http://dbpedia.org/resource/","")

        print "search term: "+uri
        try:
            query = QueryParser(Version.LUCENE_35, "dbpedia_uri", analyzer).parse(uri)
            MAX = 10000
            print "Query: "+str(query)
            result = []
            hits = searcher.search(query, MAX)
            print len(hits.scoreDocs)
            for hit in hits.scoreDocs:
                #print str(hit.score)
                #if hit.score > 2:
                doc = searcher.doc(hit.doc)
                result.append(doc.get("anchor").encode("utf-8"))
            return result
        except:
            print("Fail in "+uri)
            return []
            
    
    
    
    def index(self,path_to_index,path_files):
        'indexes files, in the moment specified to '
        #lucene.initVM()
        indexDir = path_to_index
        directory_index = SimpleFSDirectory(File(indexDir))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        writer = IndexWriter(directory_index, analyzer, True, IndexWriter.MaxFieldLength(512))
        listOfPathes = []
        listOfPathes.extend(glob.glob(path_files+"*.txt"))
        anzahl = 0
        for path_to_file in listOfPathes:
            print path_to_file
            f = open(path_to_file,"r")
            for line in f:
                entry = line.split("\t")
                anzahl+=1
                if anzahl%500000==0:
                    print anzahl
                    writer.optimize()
                doc = Document()
                #print entry[0]
                doc.add(Field("anchor", entry[0], Field.Store.YES, Field.Index.ANALYZED))
                doc.add(Field("anchor_uri", entry[1], Field.Store.YES, Field.Index.ANALYZED))
                doc.add(Field("dbpedia_uri", entry[2], Field.Store.YES, Field.Index.ANALYZED))
                doc.add(Field("number", entry[3].replace("\n",""), Field.Store.YES, Field.Index.ANALYZED))
                writer.addDocument(doc)
            writer.optimize()
         
            f.close()
            
        writer.close()
        print anzahl
        print "done"


        
