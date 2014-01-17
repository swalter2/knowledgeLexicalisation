#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os, codecs
from SPARQLWrapper import SPARQLWrapper, JSON
endpoint = "http://dbpedia.org/sparql/"
sparql = SPARQLWrapper(endpoint)

def getPairsOfGivenProperties(uri,path_to_save,language):
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
    sparql.setQuery("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT DISTINCT ?s ?z WHERE {?y <"+uri+"> ?x. ?y rdfs:label ?s. FILTER (lang(?s) = '"+language+"') . ?x rdfs:label ?z. FILTER (lang(?z) = '"+language+"')} LIMIT 30000")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    write_array = []
    for result in results["results"]["bindings"]:
        try:
            string1 = result["s"]["value"]
            string2 = result["z"]["value"]
            array.append(string1)
            array.append(string2)
            write_array.append(string1+" ## "+string2)
        except:
            pass

    
    
    if len(array)==0:
        """
        In case one have for example a DatatypeProperty, only on the left side there is a label, on the right side, there is some other value.
        It is sorted like above.
        """
        array = []
        sparql.setQuery("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT DISTINCT ?s ?x WHERE {?y <"+uri+"> ?x. ?y rdfs:label ?s. FILTER (lang(?s) = '"+language+"') .} LIMIT 30000")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
            
        for result in results["results"]["bindings"]:
            try:
                string1 = result["s"]["value"]
                string2 = result["x"]["value"]
                if string2.endswith(".0"):
                    string2 = string2.replace(".0", "")
                array.append(string1)
                array.append(string2)
                write_array.append(string1+" ## "+string2)
            except:
                pass
    print "getPairs Done"
    tmp_path = path_to_save.replace("http://dbpedia.org/property/","")
    tmp_path = tmp_path.replace("http://dbpedia.org/ontology/","")
    f_out = codecs.open(tmp_path,"w","utf-8")
    for x in write_array:
        f_out.write(x+"\n")
    f_out.close()
    print uri+" Done"
    return array
    
    
    

def getResources(language,path_to_property_file):
    try:
        os.mkdir(language)
    except:
        pass
    
    f_in = open(path_to_property_file,"r")
    for line in f_in:
        uri = line.replace("\n","")
        name = uri.replace("http://dbpedia.org/ontology/","")
        name = name.replace("http://dbpedia.org/property/","")
        path = language+"/"+name
        try:
            with open(path,"r"):
                pass

        except IOError:
            PropertyEntities = getPairsOfGivenProperties(uri,path,language)
            
    


def main():
    path_to_property_file = "train"
    path_to_property_file = "LargeScaleTest_NEW"
    getResources("de",path_to_property_file)
    getResources("es",path_to_property_file)


if __name__ == "__main__":
   main()