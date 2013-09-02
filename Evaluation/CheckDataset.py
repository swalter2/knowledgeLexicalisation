#!/usr/bin/python
import lexiconEvaluation





def run(path_gold_lexicon, property_file, output):
    print ("Start!")
    hm, number = lexiconEvaluation.createArrayEntries(path_gold_lexicon)
    print ("Read gold lexicon.")
    array_hm = []
    for key in hm:
        array_hm.append(key)
        
        
    array_property = []
    
    f_in = open(property_file,"r")
    for line in f_in:
        array_property.append(line.replace("\n",""))
    f_in.close()
    print ("Read property file")
    
    array_out = []
    
    for x in array_hm:
        if x in array_property:
            array_out.append(x)
        
    f_out = open(output,"w")
    for x in array_out:
        f_out.write(x+"\n")
    f_out.close()
    
    print "Done!"
    
    
if __name__ == '__main__':
    run("../Datasets/dbpedia_en.rdf", "../Datasets/datatype","/home/swalter/checkedDatatype")
    