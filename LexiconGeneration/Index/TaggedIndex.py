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
    Stores tagged sentences of a given corpora and will replace Index)WithID.py and Index.py
    """
    analyzer = None
    searcher = None

#    def __init__(self, path_to_index,sentencefile):
    def __init__(self, path_to_index):
        """
        Initialization
        """
        #self.index(path_to_index,sentencefile)
        global analyzer
        global searcher
        
        lucene.initVM()
        index_dir = SimpleFSDirectory(File(path_to_index))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        searcher = IndexSearcher(index_dir)

    
    def search(self,string,special = False):
        return self.searchString(string)
    
    def searchString(self, string):
        'searches for a string and returns an array of POS-tagged sentences'
        query = ""
        #print("Input String: ",string)
        try:
            MAX = 100000
            #for dates such as 1931.08.06
            string = string.replace("."," ")
            
            array = re.findall(r'[\w\s]+',string)
            string = ""
            for item in array:
                string+=item
            #print("Input String2: ",string)
            qp = QueryParser(Version.LUCENE_35, "sentence", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(string)
            #print ("query",query)
                        
            hits = searcher.search(query, MAX)
            #print len(hits)
            sentence_list = []
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                #print doc.get("sentence")
                sentence_list.append(eval(doc.get("sentence").encode("utf-8")))
            return sentence_list
        except:
            print("Fail in receiving sentence with term "+string+" in search term")
            print ("query",query)
            print "Unexpected error:", sys.exc_info()[0]
#            raw_input("wait")
            print
            return []
        
    def searchKey(self, key , rank = None):
        query = ""
        try:
            MAX = 100000
            qp = QueryParser(Version.LUCENE_35, "key", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(key)
#             print ("query",query)
                        
            hits = searcher.search(query, MAX)

            sentence_list = []
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                sentence_list.append(eval(doc.get("sentence").encode("utf-8")))
            return sentence_list
        except:
            print("Fail in receiving sentence with term "+key)
            print ("query",query)
            print "Unexpected error:", sys.exc_info()[0]
#            raw_input("wait")
            print
            return []
        

    #def index(self,path_to_index, sentencearray):
    def index(self,path_to_index,sentencearray):
        'indexes wikipedia sentences'
        lucene.initVM()
        indexDir = path_to_index
        dir = SimpleFSDirectory(File(indexDir))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        writer = IndexWriter(dir, analyzer, True, IndexWriter.MaxFieldLength(512))
        
            
        counter = 0
        for file_name in sentencearray:
            print file_name
            f = open(file_name,"r")
            for line in f:
                counter += 1
                line = line.replace("\n","")
                if "\t" in line:
                    tmp = line.split("\t")
                else:
                    tmp = [line,"0"]
                doc = Document()
                print("sentence", tmp[0])
                print ("key", tmp[1])
                print
                doc.add(Field("sentence", tmp[0], Field.Store.YES, Field.Index.ANALYZED))
                doc.add(Field("key", tmp[1], Field.Store.YES, Field.Index.ANALYZED))
    #            doc.add(IntField("key", tmp[1], Field.Store.YES, Field.Index.ANALYZED))
                writer.addDocument(doc)
                if counter%2000000 == 0:
                    writer.optimize()
                    print counter
            writer.optimize()
            f.close()
        writer.close() 
        print "Done"
        print counter


    
        
