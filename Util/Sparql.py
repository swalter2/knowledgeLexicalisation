import urllib
import re
from SPARQLWrapper import SPARQLWrapper, JSON
class Connection():
    
    #endpoint = "http://vtentacle.techfak.uni-bielefeld.de:443/sparql/"
    endpoint = "http://dbpedia.org/sparql/"
    sparql = SPARQLWrapper(endpoint)
    
    def __init__(self):
        'Initialisation'

            
        
    def fFileExist(self,psFilePath):
        'checks, if a file exists. Returns 1 if file exist and 0 if not'
   
        try:
            oFile = open(psFilePath,'r')
        except Exception:
            return 0
        else:
            oFile.close()
            return 1
   
    
    
    
#    def cleanAnswerURI(self,string):
#        answer = []
#        #print "string: "+string
#        string_array = string.split("<tr>")
#        for s in string_array:
#            m_obj = re.search(r".*<td>(.*)</td>.*", s)
#            if m_obj:
#                #the general class thing is not needed, therfore:
#                #also we are only working on dbpedia, so dbpedia has to be part of the result
#                if "owl#Thing" not in m_obj.group(1)and "dbpedia" in m_obj.group(1) and "ontology" in m_obj.group(1):
#                    answer.append(m_obj.group(1))
#        return answer
    

    
#    def cleanAnswerDouble(self, string):
#        string = string.replace("\n","")
#        #print string
#        result_array = []
#        array = string.split("</tr>  <tr>")
#        #print str(len(array))
#        for s in array:
#            while "  " in s:
#                s = s.replace("  "," ")
#            #print s
#            m_obj = re.search(r".*<td>(.*)</td> <td>(.*)</td>.*", s)
#            if m_obj:
#                string1 =  m_obj.group(1)
#                string2 =  m_obj.group(2)
#                
#                m_obj1 = re.search(r"\"(.*)\"@.*", string1)
#                if m_obj1:
#                    string1 = m_obj1.group(1) 
#                    
#                m_obj2 = re.search(r"\"(.*)\"@.*", string2)
#                if m_obj2:
#                    string2 = m_obj2.group(1)
#                    
#                result_array.append(string1)
#                result_array.append(string2)
#                #print string1
#                #print string2
#                    
#                
#                #print "\n\n"
#            #print m_obj.group(1)
#        return result_array
        

    def newsparql(self,uri):
        array = []
        
        self.sparql.setQuery("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT DISTINCT ?s ?z WHERE {?y <"+uri+"> ?x. ?y rdfs:label ?s. FILTER (lang(?s) = 'en') . ?x rdfs:label ?z. FILTER (lang(?z) = 'en')}")
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        
        for result in results["results"]["bindings"]:
            try:
#                string1 = str(result["s"]["value"])
#                string2 = str(result["z"]["value"])
                string1 = result["s"]["value"]
                string2 = result["z"]["value"]
                array.append(string1)
                array.append(string2)
            except:
                pass
            #else:
            #    pass
        
        
        if len(array)==0:
            array = []
            self.sparql.setQuery("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT DISTINCT ?s ?x WHERE {?y <"+uri+"> ?x. ?y rdfs:label ?s. FILTER (lang(?s) = 'en') .}")
            self.sparql.setReturnFormat(JSON)
            results = self.sparql.query().convert()
                
            for result in results["results"]["bindings"]:
                try:
                    
                    ###########################################
                    #
                    #
                    #TODO: eigene Methode fuer posprocessing. 1.0 zu 1=0 machen
                    #
                    #
                    ###########################################
#                    string1 = str(result["s"]["value"])
#                    string2 = str(result["x"]["value"])
                    string1 = result["s"]["value"]
                    string2 = result["x"]["value"]
                    if string2.endswith(".0"):
                        string2 = string2.replace(".0", "")
                    array.append(string1)
                    array.append(string2)
                except:
                    pass
        print "getPairs Done"
        return array
    
    def getPairsOfGivenProperties(self,uri):
        print "in getPairs"
        return self.newsparql(uri)

#            
        
    def return_class_of_resource(self,uri):
        self.sparql.setQuery("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT DISTINCT ?x WHERE {<"+uri+"> rdf:type ?x.}")
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        g_class = []
        for result in results["results"]["bindings"]:
            try:
                #print result
                g_class.append(result["x"]["value"])
                
            except:
                pass

        return g_class

    def askObjectProperty(self,uri):
        #sparql = SPARQLWrapper(endpoint)
        self.sparql.setQuery("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX owl: <http://www.w3.org/2002/07/owl#>  ASK WHERE {<"+uri+"> rdf:type owl:ObjectProperty}")
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        #print results
        for result in results:
            try:
                string = str(results[result])
                if "False" in string:
                    return False
                elif "True" in string:
                    return True


            except:
                pass
        return False
    
    def askForRange(self,uri):
        try:
            self.sparql.setQuery("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> select distinct ?x where {<"+uri+"> rdfs:range ?x}")
            self.sparql.setReturnFormat(JSON)
            results = self.sparql.query().convert()
            uri_range = None
            for result in results["results"]["bindings"]:
                uri_range = result["x"]["value"]
            return uri_range
        except:
            return None
    
    
    def askClassProperty(self,uri):
        #sparql = SPARQLWrapper(endpoint)
        self.sparql.setQuery("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX owl: <http://www.w3.org/2002/07/owl#>  ASK WHERE {<"+uri+"> rdf:type owl:Class}")
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        #print results
        for result in results:
            try:
                string = str(results[result])
                if "False" in string:
                    return False
                elif "True" in string:
                    return True


            except:
                pass
        return False

    
    
    def getLabel(self,uri):
        'returns for a given property uri the "official" name from the server '

        self.sparql.setQuery(" PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?label WHERE { <"+uri+"> rdfs:label ?label. FILTER (lang(?label) = 'en') } ")
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        label = ""
        for result in results["results"]["bindings"]:
            try:
                #print result
                label= (result["label"]["value"])
                if "(" in label:
                    label = label.split("(")[0]
                    if label.endswith(" "):
                        label = str(label[:-1])
            except:
                pass

        return [label]
