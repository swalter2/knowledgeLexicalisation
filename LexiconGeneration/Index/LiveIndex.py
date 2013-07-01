"""
Index, where the parsed sentences are stored, and live updated during parsing process.
"""
import lucene, re
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexWriter, IndexSearcher, Version, QueryParser
    
import nltk, sys, IndexUtils


class LiveIndex():
    
    analyzer = None
    searcher = None
    writer = None
    directory = None
    replace = None
    index_directory = None
    
    def __init__(self, path_to_index):
        """
        Initialisation of the Index to a given path. If Index does not exist on given path, a new Index is created
        """
        global analyzer
        global searcher
        global writer
        global index_directory
        global replace
        lucene.initVM()
        if self.does_index_exists(path_to_index)==False:
            self.create_index(path_to_index)
        
        index_directory = SimpleFSDirectory(File(path_to_index))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        searcher = IndexSearcher(index_directory)
        replace = str.replace
            
            
#    def lucene_close(self):
#        analyzer.close()
#        writer.close()
#        searcher.close()
        
    def does_index_exists(self,path_to_index):
        """
        Checks if Index already exists, returns True or False
        """
        try:
            index_directory = SimpleFSDirectory(File(path_to_index))
            analyzer = StandardAnalyzer(Version.LUCENE_35)
            writer = IndexWriter(index_directory, analyzer, False, IndexWriter.MaxFieldLength(512))
            writer.close()
            print path_to_index+" exists"
            return True
        except: 
            return False
        
    def create_index(self,path_to_index):
        """
        Creates new Index
        """
        print "Create new Index"
        path = SimpleFSDirectory(File(path_to_index))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        writer = IndexWriter(path, analyzer, True, IndexWriter.MaxFieldLength(512))
        doc = Document()
        doc.add(Field("Sentence", "Hello World", Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("X", "x", Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("Y", "y", Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("URI", "uri", Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)
        writer.close() 
    
    def tokenize(self,string):
        """
        tokenizes a sentence and returns token
        """
        return nltk.word_tokenize(string)
    
    def does_line_existQuery(self,query):
        """
        Checks, if parsed sentence already exists in index
        """

        try:
            MAX = 10
            hits = searcher.search(query, MAX)
            if len(hits.scoreDocs)>0:
                #print "query sentence: " + str(query)
                return True
            else:
                
                return False
        except:
            print "error"
            print "Unexpected error:", sys.exc_info()[0]

    def does_line_existNew(self,line,x,y):
        """
        Checks, if parsed sentence already exists in index
        """
        query = ""
        try:
            array = re.findall(r'[\w]+',line)
            string = ""
            for item in array:
                string+=item+" "
            qp = QueryParser(Version.LUCENE_35, "Sentence", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(string)
            
            MAX = 10
            hits = searcher.search(query, MAX)
            if len(hits.scoreDocs)>0:
                return True
            else:
                return False
        except Exception:
            s_tmp =  str(sys.exc_info())
            if "too many boolean clauses" in s_tmp:
                print "too many boolean clauses"
                """
                Returns true, so that the sentence is not added each time, to avoid further error messages.
                Only occours with very large sentences.
                """
                return True
            else:
                print "Unexpected error:", sys.exc_info()[0]
                print "in does line exist"
                print s_tmp
        return False

    def does_line_exist(self,line,x,y):
        """
        Old, more complex function if a sentence already exists in the index.
        Not used in the moment
        """
        return self.does_line_existNew(line, x, y)
        try:
            array = re.findall(r'[\w\s]+',x)
            x = ""
            for item in array:
                x+=item
            qp = QueryParser(Version.LUCENE_35, "X", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(x)
                        
            MAX = 100000
            hits = searcher.search(query, MAX)
            #First check, if an x already exists
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                y_entry = doc["Y"]
                if y_entry == y:
                    print "y found"
                    print
                    try:
                        array = re.findall(r'[\w\s]+',line)
                        string = ""
                        for item in array:
                            string+=item
                        qp = QueryParser(Version.LUCENE_35, "Sentence", analyzer)
                        qp.setDefaultOperator(qp.Operator.AND)
                        query = qp.parse(string)
                        MAX = 10
                        hits = searcher.search(query, MAX)
                        if len(hits.scoreDocs)>0:
                            return True
                    except Exception:
                        s_tmp =  str(sys.exc_info())
                        if "too many boolean clauses" in s_tmp:
                            print "too many boolean clauses"
                            return True
                        else:
                            print "Unexpected error:", sys.exc_info()[0]
                            print "in does line exist"
                            print s_tmp
            print 'nothing found'
            return False
        except:
            print("Fail (does line exists) in x:"+x+" y:"+y)
            print "Unexpected error:", sys.exc_info()[0]
            print

    
    
    
    def searchXYPair(self,x,y):
        """
        Returns all sentences, which are tagged with the given two entities (x,y)
        """
        tmp_hm = {}
        if x == "" or y == "":
            return []
        try:
            array = re.findall(r'[\w\s]+',x)
            x = ""
            for item in array:
                x+=item
            qp = QueryParser(Version.LUCENE_35, "X", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(x)
            MAX = 100000
            result_list = []
            hits = searcher.search(query, MAX)
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                y_entry = doc["Y"]
                if y_entry == y:
                    tmp_hm[doc["Sentence"]]=""
                    
            for key in tmp_hm:
                result_list.append(IndexUtils.sentence_wrapper(key))
            tmp_hm = {}
            return result_list
        except:
            print("Fail (search XYPair) in x:"+x+" y:"+y)
            print "Unexpected error:", sys.exc_info()[0]
            print

            
        return []
    
    
    def searchForDbpediaURI(self, uri):
        """
        Returns all sentences, which are tagged with the given DBpedia URI
        """
        print "in searchForDbpediaURI" 
        uri_old = uri
        uri = uri.replace("http://dbpedia.org/ontology/","")
        uri = uri.replace("http://dbpedia.org/property/","")
        uri = uri.replace("http://dbpedia.org/resource/","")

        array = re.findall(r'[\w\s]+',uri)
        uri = ""
        for item in array:
            uri+=item
        
        try:
            qp = QueryParser(Version.LUCENE_35, "URI", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(uri)
            print "query: "+str(query)
            MAX = 500000
            result = []
            hits = searcher.search(query, MAX)
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                dbpedia_uri = doc["URI"]
                if dbpedia_uri == uri_old:
                    result.append([IndexUtils.sentence_wrapper(doc["Sentence"]), doc["X"], doc["Y"],dbpedia_uri])
            return result
        except:
            print("Fail in uri: "+uri)
            print "Unexpected error:", sys.exc_info()[0]
            return result
        
    def searchForXY(self, uri):
        print "in searchForDbpediaURI" 
        uri_old = uri
        uri = uri.replace("http://dbpedia.org/ontology/","")
        uri = uri.replace("http://dbpedia.org/property/","")
        uri = uri.replace("http://dbpedia.org/resource/","")

        array = re.findall(r'[\w\s]+',uri)
        uri = ""
        for item in array:
            uri+=item
        hm = {}
        try:
            qp = QueryParser(Version.LUCENE_35, "URI", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(uri)
            print "query: "+str(query)
            MAX = 500000
            result = []
            hits = searcher.search(query, MAX)
            #print len(hits)
            for hit in hits.scoreDocs:
                doc = searcher.doc(hit.doc)
                dbpedia_uri = doc["URI"].encode("utf-8")
                if dbpedia_uri == uri_old:
                    x = doc["X"]
                    y = doc["Y"]
                    term = x+" "+y
                    if hm.has_key(term):
                        pass
                    else:
                        hm[term] = ""
                        result.append([x,y])
            return result
        except:
            print("Fail in uri: "+uri)
            return []
        
        
    
    def update_index_withLine(self,line,x,y,uri):
        """
        Parsed sentence is added to the index, with the corresponding two entities (x,y) and the DBpedia URI
        """
        line=line.replace("\t"," ")
        line = line.replace("\n","  ")
        line = line.replace("   ","  ")
        try:
            writer = IndexWriter(index_directory, analyzer, False, IndexWriter.MaxFieldLength(512))
            doc = Document()
            doc.add(Field("Sentence", line, Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("X", x, Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("Y", y, Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("URI", uri, Field.Store.YES, Field.Index.ANALYZED))
            writer.addDocument(doc)
            writer.optimize()
            writer.close() 
        except Exception:
            print "Unexpected error:", sys.exc_info()[0]
            raw_input("Error in updating the Sentences")
            
    
    def update_index_withLineArray(self,array):
        """
        Parsed sentences (given in an array) are added to the index, with the corresponding two entities (x,y) and the DBpedia URI
        """
        print "start adding sentences"
        writer = IndexWriter(index_directory, analyzer, False, IndexWriter.MaxFieldLength(512))
        for item in array:
            line = item[0]
            x = item[1]
            y = item[2]
            uri = item[3]
            line=line.replace("\t"," ")
            line = line.replace("\n","  ")
            line = line.replace("   ","  ")
            try:
                
                doc = Document()
                doc.add(Field("Sentence", line, Field.Store.YES, Field.Index.ANALYZED))
                doc.add(Field("X", x, Field.Store.YES, Field.Index.ANALYZED))
                doc.add(Field("Y", y, Field.Store.YES, Field.Index.ANALYZED))
                doc.add(Field("URI", uri, Field.Store.YES, Field.Index.ANALYZED))
                writer.addDocument(doc)
                
            except Exception:
                print "Unexpected error:", sys.exc_info()[0]
                raw_input("Error in updating the Sentences")
        try:
            writer.optimize()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print ("could not optimize index")

        writer.close()
        print "all sentences added"
            
        
        
    def clean_string(self, string):
        """
        Cleans Lucene query.
        """
        if string.startswith(" "):
            string = string[1:]
        array = re.findall(r'[\w\s]+',string)
        string = ""
        for item in array:
            if item.lower() !="and" and item.lower()!="or":
                string+=item
        
        while "  " in string:
            string = replace(string,"  "," ")
        string = replace(string,"  "," ")
        string = replace(string," ", " AND ")
        string = replace(string,"AND AND","AND")
        string = replace(string,"AND  AND","AND")
        if string.startswith(" AND "):
            string = string[5:]
        if string.endswith(" "):
            string = string[:-1]
        if string.endswith("AND"):
            string = string[:-3]
            
        return string 
        
  
