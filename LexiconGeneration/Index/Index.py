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
    replace = None
    
    def __init__(self, path_to_index):
        """
        Initialization
        """
        global analyzer
        global searcher
        
        lucene.initVM()
        index_dir = SimpleFSDirectory(File(path_to_index))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        searcher = IndexSearcher(index_dir)
        global replace
        replace = str.replace
    

    def clean_string(self, string):
        """
        creates search string and also cleans string up, so nasty errors are avoided
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

    def search(self, string ,special = None):
        query = ""
        try:
            MAX = 100000
            #for dates such as 1931.08.06
            string = string.replace("."," ")
            
            array = re.findall(r'[\w\s]+',string)
            string = ""
            for item in array:
                string+=item
            qp = QueryParser(Version.LUCENE_35, "title", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(string)
#            print ("query",query)
                        
            hits = searcher.search(query, MAX)
            
            sentence_list = []
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                sentence_list.append(doc.get("title").encode("utf-8"))
            return sentence_list
        except:
            print("Fail in receiving sentence with term "+string)
            print ("query",query)
            print "Unexpected error:", sys.exc_info()[0]
#            raw_input("wait")
            print
            return []
    
#    def index(self):
#        'indexes wikipedia sentences'
#        lucene.initVM()
#        indexDir = [path]
#        dir = SimpleFSDirectory(File(indexDir))
#        analyzer = StandardAnalyzer(Version.LUCENE_35)
#        writer = IndexWriter(dir, analyzer, True, IndexWriter.MaxFieldLength(512))
#        file_name = [path/file_name]
#            
#            
#        f = open(file_name,"r")
#        for line in f:
#            line = line.replace("\n","")
#            doc = Document()
#            doc.add(Field("title", line, Field.Store.YES, Field.Index.ANALYZED))
#            writer.addDocument(doc)
#        writer.close() 
#        f.close()


    
        
