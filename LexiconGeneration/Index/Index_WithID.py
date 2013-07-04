"""
Used PyLucene Implementation: http://www.apache.org/dist/lucene/pylucene/pylucene-3.6.0-2-src.tar.gz
"""

import lucene, sys
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, IndexSearcher, Version, QueryParser
import re

class LuceneIndex():
    """
    Stores the sentences of the given corpora
    """
    analyzer = None
    searcher = None

    
    def __init__(self, path_to_index):
#    def __init__(self):
        """
        Initialization
        """
#        self.index()
        global analyzer
        global searcher
        
        lucene.initVM()
        index_dir = SimpleFSDirectory(File(path_to_index))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        searcher = IndexSearcher(index_dir)

    

    def search(self, string , special = None):
        print ("special in search",str(special))
        if special == True:
            print "in search"
            #here then string is a list of keys
            return self.search_two_keys(string)
        query = ""
        try:
            MAX = 100000
            #for dates such as 1931.08.06
            string = string.replace("."," ")
            
            array = re.findall(r'[\w\s]+',string)
            string = ""
            for item in array:
                string+=item
            qp = QueryParser(Version.LUCENE_35, "sentence", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(string)
            print ("query",query)
                        
            hits = searcher.search(query, MAX)

            sentence_list = []
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                sentence_list.append(doc.get("sentence").encode("utf-8"))
            return sentence_list
        except:
            print("Fail in receiving sentence with term "+string)
            print ("query",query)
            print "Unexpected error:", sys.exc_info()[0]
#            raw_input("wait")
            print
            return []
        
    def search_key(self, key , rank = None):
        query = ""
        try:
            MAX = 100000
            qp = QueryParser(Version.LUCENE_35, "key", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(key)
            print ("query",query)
                        
            hits = searcher.search(query, MAX)

            sentence_list = []
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                sentence_list.append(doc.get("sentence").encode("utf-8"))
            return sentence_list
        except:
            print("Fail in receiving sentence with term "+key)
            print ("query",query)
            print "Unexpected error:", sys.exc_info()[0]
#            raw_input("wait")
            print
            return []
        
    def search_two_keys(self, keys ,rank = None):
        print ("reached special search")
        query = ""
        sentence_list = []
        try:
            MAX = 100000

            for key in keys:
                qp = QueryParser(Version.LUCENE_35, "key", analyzer)
                qp.setDefaultOperator(qp.Operator.AND)
                query = qp.parse(key)
                            
                hits = searcher.search(query, MAX)
    
                
                for hit in hits.scoreDocs:
                    doc = searcher.doc(hit.doc)
                    sentence_list.append(doc.get("sentence").encode("utf-8"))
            
        except:
            print("Fail in receiving sentence with term "+key)
            print ("query",query)
            print "Unexpected error:", sys.exc_info()[0]
#            raw_input("wait")
            print
        print "special search done"
        return sentence_list
    
    def index(self):
        'indexes wikipedia sentences'
        lucene.initVM()
        indexDir = "/home/swalter/Development/NeuerIndex1"
        dir = SimpleFSDirectory(File(indexDir))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        writer = IndexWriter(dir, analyzer, True, IndexWriter.MaxFieldLength(512))
        file_name = "/home/swalter/list_of_sentences"
            
        counter = 0
        
        f = open(file_name,"r")
        for line in f:
            counter += 1
            line = line.replace("\n","")
            tmp = line.split("\t")
            doc = Document()
            print tmp[0]
            print tmp[1]
            doc.add(Field("sentence", tmp[0], Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("key", tmp[1], Field.Store.YES, Field.Index.ANALYZED))
#            doc.add(IntField("key", tmp[1], Field.Store.YES, Field.Index.ANALYZED))
            writer.addDocument(doc)
            if counter%2000000 == 0:
                writer.optimize()
                print counter
        writer.optimize()
        writer.close() 
        f.close()
        print "Done"


    
        
