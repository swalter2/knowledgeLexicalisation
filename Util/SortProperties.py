from LexiconGeneration import Sparql
#
sparql = Sparql.Connection()
#path = "Datasets/en_lexicalizedURIs"
#
#f_in = open(path,"r")
#hm_object = {}
#hm_class = {}
#hm_datatype = {}
#counter = 0
#for line in f_in:
#    counter += 1
#    uri = "http://dbpedia.org/ontology/"+line.replace("\n","")
#    print uri
#    if sparql.askClassProperty(uri) == True:
#        hm_class[uri] = ""
#    elif sparql.askObjectProperty(uri) == True:
#        hm_object[uri] = ""
#    else:
#        hm_datatype[uri] = ""
#        
#f_in.close()
#       
#print ("object",len(hm_object))
#print ("class", len(hm_class))
#print ("datatype",len(hm_datatype))
#print ("overall",counter)
#
#f_out = open("Datasets/classes","w")
#for key in hm_class:
#    f_out.write(key+"\n")
#f_out.close()
#
#f_out = open("Datasets/object","w")
#for key in hm_object:
#    f_out.write(key+"\n")
#f_out.close()
#
#f_out = open("Datasets/datatype","w")
#for key in hm_datatype:
#    f_out.write(key+"\n")
#f_out.close()

path = "Datasets/datatype"

f_in = open(path,"r")
hm = {}
for line in f_in:
    uri = line.replace("\n","")
    tmp = sparql.askForRange(uri)
    hm[tmp] = ""
f_in.close()
for key in hm:
    print key
    
    
#List of used ranges in the used datatype properties.
#http://dbpedia.org/datatype/engineConfiguration
#http://www.w3.org/2001/XMLSchema#string
#http://www.w3.org/2001/XMLSchema#integer
#http://www.w3.org/2001/XMLSchema#positiveInteger
#http://www.w3.org/2001/XMLSchema#float
#http://www.w3.org/2001/XMLSchema#nonNegativeInteger
#http://www.w3.org/2001/XMLSchema#date
#http://www.w3.org/2001/XMLSchema#gYear
#http://www.w3.org/2001/XMLSchema#double
#http://www.w3.org/2001/XMLSchema#anyURI
#
##boolean
#
#Get all ranges for all datatypeProperties in dbpedia
#PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  SELECT DISTINCT ?y WHERE {?x rdf:type owl:DatatypeProperty . ?x rdfs:range ?y}
#
#http://dbpedia.org/datatype/minute
#http://dbpedia.org/datatype/litre
#http://dbpedia.org/datatype/millimetre
#http://dbpedia.org/datatype/second
#http://dbpedia.org/datatype/gramPerKilometre
#http://dbpedia.org/datatype/cubicCentimetre
#http://dbpedia.org/datatype/kilowatt
#http://dbpedia.org/datatype/kilometrePerHour
#http://dbpedia.org/datatype/newtonMetre
#http://dbpedia.org/datatype/kilogram
#http://dbpedia.org/datatype/squareMetre
#http://dbpedia.org/datatype/metre
#http://dbpedia.org/datatype/kelvin
#http://dbpedia.org/datatype/kilogramPerCubicMetre
#http://dbpedia.org/datatype/kilometre
#http://dbpedia.org/datatype/kilometrePerSecond
#http://dbpedia.org/datatype/day
#http://dbpedia.org/datatype/squareKilometre
#http://dbpedia.org/datatype/cubicKilometre
#http://dbpedia.org/datatype/inhabitantsPerSquareKilometre
#http://dbpedia.org/datatype/cubicMetre
#http://dbpedia.org/datatype/centimetre
#http://dbpedia.org/datatype/megabyte
#http://dbpedia.org/datatype/hour
#http://dbpedia.org/datatype/cubicMetrePerSecond
#http://www.w3.org/2001/XMLSchema#string
#http://www.w3.org/2001/XMLSchema#double
#http://www.w3.org/2001/XMLSchema#gYear
#http://www.w3.org/2001/XMLSchema#date
#http://www.w3.org/2001/XMLSchema#nonNegativeInteger
#http://www.w3.org/2001/XMLSchema#positiveInteger
#http://www.w3.org/2001/XMLSchema#float
#http://www.w3.org/2001/XMLSchema#boolean
#http://www.w3.org/2001/XMLSchema#integer
#http://dbpedia.org/datatype/engineConfiguration
#http://dbpedia.org/datatype/fuelType
#http://www.w3.org/2001/XMLSchema#anyURI
#http://www.w3.org/2001/XMLSchema#gYearMonth
#http://dbpedia.org/datatype/valvetrain
