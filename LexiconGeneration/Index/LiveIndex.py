#You will have to open the index without overwriting thus:

#IndexWriter writer = new IndexWriter("MyIndexPath",analyzer, false);
#The false flag at the end tells it to open in append mode.

#The writer has an UpdateDocument method

#writer.UpdateDocument(new Term("IDField",id), doc);
#the id field should be some unique document identifier such as filename or file number etc.
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
        global analyzer
        global searcher
        global writer
        global index_directory
        global replace
        lucene.initVM()
        if self.test_existens_index(path_to_index)==False:
            self.create_index(path_to_index)
        
        index_directory = SimpleFSDirectory(File(path_to_index))
        analyzer = StandardAnalyzer(Version.LUCENE_35)
        searcher = IndexSearcher(index_directory)
        replace = str.replace
        #Has to be set to False, because we want to write into an existing Index
        #writer = IndexWriter(index_directory, analyzer, False, IndexWriter.MaxFieldLength(512))
            
            
    def lucene_close(self):
        analyzer.close()
        writer.close()
        searcher.close()
        
    def test_existens_index(self,path_to_index):
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
        'tokenizes a sentence and returns token'
        return nltk.word_tokenize(string)
    
    def does_line_existQuery(self,query):

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
        query = ""
        #line = line.replace("'"," ")
        try:
            #array = re.findall(r'[\w\s]+',line)
            array = re.findall(r'[\w]+',line)
            string = ""
            for item in array:
                string+=item+" "
#                print item
#            print string
            #query = QueryParser(Version.LUCENE_35, "Sentence", analyzer).parse(line)
            qp = QueryParser(Version.LUCENE_35, "Sentence", analyzer)
            qp.setDefaultOperator(qp.Operator.AND)
            query = qp.parse(string)
            
            MAX = 10
            hits = searcher.search(query, MAX)
            if len(hits.scoreDocs)>0:
                return True
            else:
                #print "query False sentence: " + str(query)
                return False
        except Exception:
            s_tmp =  str(sys.exc_info())
            if "too many boolean clauses" in s_tmp:
                print "too many boolean clauses"
                return True
            else:
                print "Unexpected error:", sys.exc_info()[0]
                print "in does line exist"
                print s_tmp
#        print "nothing found"
        return False

    def does_line_exist(self,line,x,y):
        return self.does_line_existNew(line, x, y)
        try:
            #query = QueryParser(Version.LUCENE_35, "X", analyzer).parse(x)
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
                #then if there is the already corresponding y
                if y_entry == y:
                    print "y found"
                    print
                    #and only if both above are true, make the "big search" with the line
                    try:
                        array = re.findall(r'[\w\s]+',line)
                        string = ""
                        for item in array:
                            string+=item
                        #query = QueryParser(Version.LUCENE_35, "Sentence", analyzer).parse(line)
                        qp = QueryParser(Version.LUCENE_35, "Sentence", analyzer)
                        qp.setDefaultOperator(qp.Operator.AND)
                        query = qp.parse(string)
#                        print "query sentence: " + str(query)
                        MAX = 10
                        hits = searcher.search(query, MAX)
                        if len(hits.scoreDocs)>0:
                            print
                            print "##### TRUE #####"
                            print
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
    
    
    
    def searchXYPair(self,x,y):
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
                    #result_list.append([doc.get("Sentence").encode("utf-8"),doc.get("X"),y_entry]) 
                    #result_list.append(IndexUtils.sentence_wrapper(doc["Sentence"])) 
                    tmp_hm[doc["Sentence"]]=""
                    
            for key in tmp_hm:
                result_list.append(IndexUtils.sentence_wrapper(key))
            tmp_hm = {}
            return result_list
        except:
            print("Fail (search XYPair) in x:"+x+" y:"+y)
        return []
    
    
    def searchForDbpediaURI(self, uri):
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
            #query = QueryParser(Version.LUCENE_35, "dbpedia_uri", analyzer).parse(uri)
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
                    result.append([IndexUtils.sentence_wrapper(doc["Sentence"]), doc["X"], doc["Y"],dbpedia_uri])
            return result
        except:
            print("Fail in uri: "+uri)
            return []
        
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
            #query = QueryParser(Version.LUCENE_35, "dbpedia_uri", analyzer).parse(uri)
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
        line=line.replace("\t"," ")
        line = line.replace("\n","  ")
        line = line.replace("   ","  ")
#        print "########################"
#        print line
#        print x
#        print y
        try:
            writer = IndexWriter(index_directory, analyzer, False, IndexWriter.MaxFieldLength(512))
            doc = Document()
            doc.add(Field("Sentence", line, Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("X", x, Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("Y", y, Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("URI", uri, Field.Store.YES, Field.Index.ANALYZED))
            #print "came here"
            writer.addDocument(doc)
            writer.optimize()
            writer.close() 
        #print "\n\n"
        except Exception:
            print "Unexpected error:", sys.exc_info()[0]
            raw_input("Error in updating the Sentences")
            
    
    def update_index_withLineArray(self,array):
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
                #print "came here"
                writer.addDocument(doc)
                
            #print "\n\n"
            except Exception:
                print "Unexpected error:", sys.exc_info()[0]
                raw_input("Error in updating the Sentences")
        writer.optimize()
        writer.close()
        print "all sentences added"
            
            
            
#    def update_index_withLineArray(self,parsed_sentences):
#        add_counter = 0
#        error_counter = 0
#        writer = IndexWriter(dir, analyzer, False, IndexWriter.MaxFieldLength(512))
#        #print "created writer"
#        
#        for item in parsed_sentences:
#            sentence = item
#            sentence=sentence.replace("\t"," ")
#            sentence=sentence.replace("\n"," ")
#            
#            
#            try:
#                doc = Document()
#                doc.add(Field("title", sentence, Field.Store.YES, Field.Index.ANALYZED))
#                writer.addDocument(doc)
#                add_counter += 1
#                #print "added"
#            except:
#                error_counter += 1
#    
#        
#        writer.optimize()
#        writer.close() 
#        return add_counter, error_counter
        
        
    def clean_string(self, string):
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
            
        #raw_input(string)
        return string 
        
  
