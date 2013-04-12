def read_ontology(path):
    f = file(path,"r")
    
    class_list = {}
    property_list = {}
    
    for line in f:
        if "owl:ObjectProperty rdf:about=" in line:
            line = line.replace("owl:ObjectProperty rdf:about=","")
            line = line.replace("\n","")
            line = line.replace("Ontology1336387504255;","http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#")
            line = line.replace("<\"&","")
            line = line.replace("\">","")   
            line = line.replace("\"/>","") 
            line = line.replace("\t","")
            line = line.replace(" ","")    
            property_list[line]=""
            #print line
            
        elif "owl:DatatypeProperty rdf:about=" in line:
            line = line.replace("owl:DatatypeProperty rdf:about=","")
            line = line.replace("\n","")
            line = line.replace("Ontology1336387504255;","http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#")
            line = line.replace("<\"&","")
            line = line.replace("\">","")    
            line = line.replace("\t","")
            line = line.replace("\"/>","")
            line = line.replace(" ","")        
            property_list[line]=""
            #print line    
        elif "owl:Class rdf:about=" in line:
            line = line.replace("owl:Class rdf:about=","")
            line = line.replace("\n","")
            line = line.replace("Ontology1336387504255;","http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#")
            line = line.replace("<\"&","")
            line = line.replace("\">","")    
            line = line.replace("\t","")
            line = line.replace("\"/>","")
            line = line.replace(" ","")        
            class_list[line]=""
            #print line
            
    return class_list, property_list
