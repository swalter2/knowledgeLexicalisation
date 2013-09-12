from SPARQLWrapper import SPARQLWrapper, JSON
endpoint = "http://dbpedia.org/sparql/"
sparql = SPARQLWrapper(endpoint)

def getPairsOfGivenProperties(uri):
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
    sparql.setQuery("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT DISTINCT ?s ?z WHERE {?y <"+uri+"> ?x. ?y rdfs:label ?s. FILTER (lang(?s) = 'en') . ?x rdfs:label ?z. FILTER (lang(?z) = 'en')} LIMIT 30000")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    for result in results["results"]["bindings"]:
        try:
            string1 = result["s"]["value"]
            string2 = result["z"]["value"]
            array.append(string1+" ## " + string2)
        except:
            pass
    
    if len(array)==0:
        """
        In case one have for example a DatatypeProperty, only on the left side there is a label, on the right side, there is some other value.
        It is sorted like above.
        """
        array = []
        sparql.setQuery("PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT DISTINCT ?s ?x WHERE {?y <"+uri+"> ?x. ?y rdfs:label ?s. FILTER (lang(?s) = 'en') .} LIMIT 30000")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
            
        for result in results["results"]["bindings"]:
            try:
                string1 = result["s"]["value"]
                string2 = result["x"]["value"]
                if string2.endswith(".0"):
                    string2 = string2.replace(".0", "")
                array.append(string1+" ## " + string2)

            except:
                pass
    print "getPairs Done"
    return array




def main():
    path = "Path"
    max_counter = 0
    f_in = open(path+"/counter.txt","r")
    for line in f_in:
        max_counter = int(line.replace("\n",""))
    f_in.close()
#    uri.txt is a list of dbpedia uris
    f_in = open(path+"/uri.txt","r")
    hm = {}
    try:
        f_out = open(path+"/returnedentities.txt","r")
        for line in f_out:
            hm[line.replace("\n","")] = ""
        f_out.close() 
    except:
        pass
    f_out = open(path+"/returnedentities.txt","w")
    for key in hm:
        try:
            f_out.write(key+"\n")
        except:
            pass
    f_out.close()
    counter = 0
    for line in f_in:
        counter += 1
        if counter > max_counter:
            uri = line.replace("\n","")
            print uri
            array = getPairsOfGivenProperties(uri)
    
            for x in array:
                hm[x] = ""
#            saves all entities of all uris in one file
            f_out = open(path+"/returnedentities.txt","w")
            for key in hm:
                try:
                    f_out.write(key+"\n")
                except:
                    pass
            f_out.close()
#            saves the entities for each single uri
            f_out = open(path+"/ResourceFolder/"+uri.replace("http://dbpedia.org/ontology/",""),"w")
            for x in array:
                try:
                    f_out.write(x+"\n")
                except:
                    pass
            f_out.close()
            
            f_out = open(path+"/counter.txt","w")
            f_out.write(str(counter))
            f_out.close()
            
            
            
main()