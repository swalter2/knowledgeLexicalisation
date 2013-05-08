"""
Used PyLucene Implementation: http://www.apache.org/dist/lucene/pylucene/pylucene-3.6.0-2-src.tar.gz
"""

import lucene
from lucene import \
SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, IndexSearcher, Version, QueryParser
import re, glob

class LuceneIndex():
    """
    Stores the Anchors text created from Wikipedia
    """
    analyzer = None
    searcher = None
    replace = None
    
    def __init__(self, path_to_index):
        """
        Initialization
        """
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
        """
        Cleans string and creates Lucene query
        """
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
        """
        searches for anchor text, given a label and returns the anchor itself, the anchor-uri, the corresponding of the head dbpedia-uri 
        and the number of frequency, how often this anchor text occourred in the english Wikipedia.
        """

        string = self.clean_string(string)
        try:
            query = QueryParser(Version.LUCENE_35, "anchor", analyzer).parse(string)
            MAX = 10000
            result = []
            hits = searcher.search(query, MAX)
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                result.append([doc.get("anchor").encode("utf-8"), doc.get("anchor_uri").encode("utf-8"), doc.get("dbpedia_uri").encode("utf-8"), doc.get("number").encode("utf-8")])
            return result
        except:
            print("Fail in "+string)
            return []
            
    def searchExactAnchor(self, string):
        """
        searches for anchor text, given a label (exact label match, not partial label match) and returns the anchor itself, the anchor-uri, the corresponding of the head DBpedia-uri 
        and the number of frequency, how often this anchor text occurred in the english Wikipedia.
        """
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
        """
        Returns all anchor texts, which are related to the given DBpedia URI.
        Also returns for each anchor text the corresponding URI and the number of how often the anchor appears on the english Wikipedia
        """
        uri_old = uri
        uri = uri.replace("http://dbpedia.org/resource/","")

        array = re.findall(r'[\w\s]+',uri)
        uri = ""
        for item in array:
            uri+=item
        
        try:
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
            
    def searchForDbpediaURImax(self, uri, number):
        """
        Returns maximal the number of anchor texts, which are related to the given DBpedia URI.
        Also returns for each anchor text the corresponding URI and the number of how often the anchor appears on the English Wikipedia
        """
        uri_old = uri
        uri = uri.replace("http://dbpedia.org/resource/","")

        array = re.findall(r'[\w\s]+',uri)
        uri = ""
        for item in array:
            uri+=item
        
        try:
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
            
            result = sorted(result, key = itemgetter(1), reverse=True)
            if len(result) > number:
                return result[0:number]
        
            else:
                return result
            
            return result
        except:
            print("Fail in uri: "+uri)
            return []
        
    def searchForDbpediaURIreturnAnchor(self, uri):
        """
        Returns only all anchor texts, which are related to the given DBpedia URI.
        """

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
        'indexes anchor texts from a given folder'
        #lucene.initVM()
        indexDir = path_to_index
        directory_index = SimpleFSDirectory(File(indexDir))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        writer = IndexWriter(directory_index, analyzer, True, IndexWriter.MaxFieldLength(512))
        listOfPathes = []
        listOfPathes.extend(glob.glob(path_files+"*.txt"))
        counter = 0
        for path_to_file in listOfPathes:
            print path_to_file
            f = open(path_to_file,"r")
            for line in f:
                entry = line.split("\t")
                counter+=1
                """
                optimizes index after a certain amount of added documents
                """
                if counter%500000==0:
                    print counter
                    writer.optimize()
                doc = Document()
                doc.add(Field("anchor", entry[0], Field.Store.YES, Field.Index.ANALYZED))
                doc.add(Field("anchor_uri", entry[1], Field.Store.YES, Field.Index.ANALYZED))
                doc.add(Field("dbpedia_uri", entry[2], Field.Store.YES, Field.Index.ANALYZED))
                doc.add(Field("number", entry[3].replace("\n",""), Field.Store.YES, Field.Index.ANALYZED))
                writer.addDocument(doc)
            writer.optimize()
         
            f.close()
            
        writer.close()
        print counter
        print "done"


        
