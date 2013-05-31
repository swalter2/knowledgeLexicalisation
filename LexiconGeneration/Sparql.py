import urllib
import re
from SPARQLWrapper import SPARQLWrapper, JSON
class Connection():
    """
    SPARQL class which provides the connection between system and SPARQL-endpoint
    """
    
    endpoint = "http://vtentacle.techfak.uni-bielefeld.de:443/sparql/"
    #endpoint = "http://dbpedia.org/sparql/"
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
   
    
        

    #def newsparql(self,uri):
    def getPairsOfGivenProperties(self,uri):
        """
        returns all entities of a given properties in one array.
        Barack Obama
        Michele Obama
        .
        .
        .
        So that always two entries are representing the two entries from a property
        """
        array = []
        """
        This function, if both entities are string based.
        Also only the English label is returned yet.
        """
        self.sparql.setQuery("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT DISTINCT ?s ?z WHERE {?y <"+uri+"> ?x. ?y rdfs:label ?s. FILTER (lang(?s) = 'en') . ?x rdfs:label ?z. FILTER (lang(?z) = 'en')}")
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        
        for result in results["results"]["bindings"]:
            try:
                string1 = result["s"]["value"]
                string2 = result["z"]["value"]
                array.append(string1)
                array.append(string2)
            except:
                pass

        
        
        if len(array)==0:
            """
            In case one have for example a DatatypeProperty, only on the left side there is a label, on the right side, there is some other value.
            It is sorted like above.
            """
            array = []
            self.sparql.setQuery("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT DISTINCT ?s ?x WHERE {?y <"+uri+"> ?x. ?y rdfs:label ?s. FILTER (lang(?s) = 'en') .}")
            self.sparql.setReturnFormat(JSON)
            results = self.sparql.query().convert()
                
            for result in results["results"]["bindings"]:
                try:
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
    
#    def getPairsOfGivenProperties(self,uri):
#        print "in getPairs"
#        return self.newsparql(uri)

            
        
    def return_class_of_resource(self,uri):
        """
        Returns all classes, a resource is linked to.
        For example Start Trek Nemesis is part of the classes:
        http://www.w3.org/2002/07/owl#Thing
        http://de.dbpedia.org/ontology/Work
        http://schema.org/CreativeWork
        http://de.dbpedia.org/ontology/Film
        http://schema.org/Movie
        """
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
        """
        Checks, if a given property is from the type ObjectProperty
        """
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
        """
        returns the range of a given property
        """
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
        """
        Checks, if a given property is from the type class
        """
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
        """
        returns the label for a given property
        """

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