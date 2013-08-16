#!/usr/bin/python
import os, re, sys, ConfigParser
from time import time
from LexiconGeneration import Sparql
from LexiconGeneration import LexiconGenerator
from LexiconGeneration import Approach1
from Evaluation import lexiconEvaluation 
from subprocess import Popen, PIPE, STDOUT


#from LexiconGeneration.Parser import MaltParser
from LexiconGeneration.Index import Index, LiveIndex, AnchorIndex, Index_WithID

#m_parser = None
index = None
parsed_sentence_index = None
anchor_index = None
en_de_lexicon = {}
    
    

def generateEnDeLexicon():
    lexicon = {}
    f_in = open("Util/de-en.txt")
    #das A und O [ugs.] :: the nuts and bolts [coll.]
    for line in f_in:
        if line.startswith("#"):
            pass
        else:
            line = line.replace("\n","")
            tmp = line.split(" :: ")
            german = tmp[0]
            english = tmp[1]
            
            #only singular
            if "|" in german:
                german = german.split("|")[0]
                
            if "|" in english:
                english = english.split("|")[0]
            if "[" in german:
                german = german.split("[")[0]
            if "(" in german:
                german = german.split("(")[0]
            german = german.replace("{f}","")
            german = german.replace("{m}","")
            german = german.replace("{n}","")
            german = german.replace("  "," ")
            german = german.replace("\xc3\xbc","ue")
            german = german.replace("\xc3\xa4","ae")
            german = german.replace("\xc3\x9f","ss")
            german = german.replace("\xc3\xb6","oe")
            if german.endswith(" "):
                german = german[:-1]
            german = german.lower()
            
            for x in english.split(";"):
                if x.startswith(" "):
                    x = x[1:]
                if x.endswith(" "):
                    x = x[:-1]
                if " (" in x:
                    x = x.split(" (")[0]
                x = x.lower()
                if lexicon.has_key(x):
                    tmp = lexicon[x]
                    for t in german.split(" ; "):
                        tmp.append(t)
                    lexicon[x] = tmp
                else:
                    lexicon[x] = german.split(" ; ")
            
    return lexicon
        
        
def _init_():
    """
    Initialisation of the Index and the Parser
    """
    print "start initialisation"
    
    global index
    global parsed_sentence_index
    global en_de_lexicon
    en_de_lexicon = generateEnDeLexicon()
    
    config = ConfigParser.ConfigParser()
    config.read('config.conf')

    
    special = False
    #Set paths to the correct target language
    path_to_index = ""
    path_to_parsed_sentences_index = ""
    if config.get('system_language', 'language') == "English":
        path_to_index = config.get('index', 'wikipedia_index_english');
        path_to_parsed_sentences_index = config.get('index', 'wikipedia_live_index_english')
    if config.get("index","advancedEnglishIndex") == "True" and config.get('system_language', 'language') == "English":
        path_to_parsed_sentences_index = config.get('index', 'wikipedia_live_index_english')
        path_to_index = config.get('index', 'advanced_wikipedia_index_english')
        
        special = True
    
    elif config.get('system_language', 'language') == "German":
        path_to_index = config.get('index', 'wikipedia_index_german');
        path_to_parsed_sentences_index = config.get('index', 'wikipedia_live_index_german')
        
    #create Indexes
    print ("path_to_parsed_sentences_index",path_to_parsed_sentences_index)
    print ("path_to_index",path_to_index)
    if special == False:
        index = Index.LuceneIndex(path_to_index)
    else:
        index = Index_WithID.LuceneIndex(path_to_index)
        
    parsed_sentence_index = LiveIndex.LiveIndex(path_to_parsed_sentences_index)
    
    global anchor_index
    #in the moment extracted from the English Wikipedia, has to be adapted for each language
    anchor_index = AnchorIndex.LuceneIndex(config.get('index', 'anchor_index'))
    
    print "initialisation done"
    
    
    


def run_and_evaluate(list_of_properties,path_goldstandard,path,parse_flag):

    sparql=Sparql.Connection()
    t1= time()
    
    
    timestemp = str(t1)
    timestemp = timestemp.replace(".","")
    timestemp = timestemp[2:9]
    if not path.endswith("/"):
        path += "/"
    
    path += "Global"+timestemp+"/"
    os.mkdir(path)
    original_path = path
    lemonEntriesHm = {}
    f_in = open(list_of_properties,"r")
    property_counter = 0
    for line in f_in:
        property_counter += 1
        uri = line.replace("\n","")
        path = original_path
        label = sparql.getLabel(uri)[0]
        label = label.replace(" ","+")
        path += label+"Results"
        os.mkdir(path)
    
        web_string = "<html><head><meta http-equiv=\"content-type\" content=\"text/html; charset=ISO-8859-1\"><title>Pattern overview</title></head><body><h2>Pattern overview</h2>"
       
        string =""
        tmp_hm = {}
        print uri
        if sparql.askClassProperty(uri) == True:
           entryArray = LexiconGenerator.createClassEntry(uri,en_de_lexicon)
           for entry in entryArray:
               lemonEntriesHm[entry] = ""
        else:
            string, tmp_hm = Approach1.creatingLexiconEntry_for_singleURI(False, uri, parse_flag, path, index,parsed_sentence_index,anchor_index,en_de_lexicon)
            for key in tmp_hm:
               lemonEntriesHm[key] = ""   
               
        string += "Time for this property: "+str((time()-t1)/60.0)+" minutes"
        string += "<p><a href=\"Lemon"+label+"\"> LemonEntry for "+label+" </a></p>"
   
        web_string += "<p> <p>"+string+"</p>  </p>"
   
        web_string += "</body></html>"
   
        f=file(path+"index.html","w")
        f.write(web_string)
        f.close()
       
    #######################
    #
    # Write Lexicon
    #
    #######################    
#     write_lexicon(original_path,lemonEntriesHm)
    write_pattern_lexicon(original_path,lemonEntriesHm)

   
   #####################
   ##
   ## use lemonpatterns to create out of the .ldp file a working rdf file
   ##
   #####################
   
   #lemonpatterns input output
   #output => evaluation
    #os.system("lemonpatterns "+original_path+"PatternLexicon.ldp lemlexicon.rdf")
    shell_command = "bash -i -c \"lemonpatterns "+original_path+"PatternLexicon.ldp "+original_path+"lemlexicon.rdf\""
    event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, 
    stderr=STDOUT)
    
    output = event.communicate()
    event.wait()
   
    print ("output",str(output))
    print "lexicon generated"
    #######################
    #
    # Do evaluation
    #
    ######################
#     lexiconEvaluation.evaluate(original_path+"LemLexicon.ttl",True,path_goldstandard,property_counter)
    lexiconEvaluation.evaluate(original_path+"lemlexicon.rdf",True,path_goldstandard,property_counter)


    print "\n\n DONE"
    
    

def run(uri,path,parse_flag):
    """
    Executes the patterngeneration process.
    Input is the given URI, the path where the results has to be parsed, and also the parse_flag, which indicates,if new sentences have to be parsed (TRUE),
    or if already parsed sentences from the Index will be used(FALSE).
    """
    sparql=Sparql.Connection()
    t1= time()
    label = sparql.getLabel(uri)[0]
    label = label.replace(" ","+")
    
    
    timestemp = str(t1)
    timestemp = timestemp.replace(".","")
    timestemp = timestemp[2:9]
    if not path.endswith("/"):
        path += "/"
    
    path += label+timestemp+"/"
    os.mkdir(path)
     
    original_path = path
    os.mkdir(path+"Result")

    lemonEntriesHm = {}

    web_string = "<html><head><meta http-equiv=\"content-type\" content=\"text/html; charset=ISO-8859-1\"><title>Pattern overview</title></head><body><h2>Pattern overview</h2>"
   
    string =""
    tmp_hm = {}
   
    if sparql.askClassProperty(uri) == True:
       entryArray = LexiconGenerator.createClassEntry(uri,en_de_lexicon)
       for entry in entryArray:
           lemonEntriesHm[entry] = ""
    else:
        string, tmp_hm = Approach1.creatingLexiconEntry_for_singleURI(False, uri, parse_flag, path, index,parsed_sentence_index,anchor_index,en_de_lexicon)
        for key in tmp_hm:
           lemonEntriesHm[key] = ""   
       
    #######################
    #
    # Write Lexicon
    #
    #######################    
    write_lexicon(original_path,lemonEntriesHm)
   

    string += "Time for this property: "+str((time()-t1)/60.0)+" minutes"
    string += "<p><a href=\"Lemon"+label+"\"> LemonEntry for "+label+" </a></p>"
   
    web_string += "<p> <p>"+string+"</p>  </p>"
   
    web_string += "</body></html>"
   
    f=file(path+"index.html","w")
    f.write(web_string)
    f.close()

    print "\n\n DONE"
    
    
    
def write_pattern_lexicon(original_path,lemonEntriesHm): 
    f_out = file(original_path+"PatternLexicon.ldp","w")
    lexicon = "@prefix dbpedia:  <http://dbpedia.org/ontology/> .\n"
    lexicon += "@prefix resource: <http://dbpedia.org/resource/> .\n"
    lexicon += "@prefix lex: <http://github.com/cunger/lemon.dbpedia/target/dbpedia_all#> .\n"
    lexicon += "Lexicon(<http://github.com/cunger/lemon.dbpedia/target/dbpedia_en_8#>,\"en\",\n"
    for key in lemonEntriesHm:
        lexicon += key+",\n"
    #remove final ,\n
    lexicon = lexicon[:-3]
    lexicon += "))"
    
    f_out.write(lexicon)
    f_out.close()
    
    
def write_lexicon(original_path,lemonEntriesHm):
    """
    Writes the Lemonentries to a file on a given path
    Turtle syntax
    """
    f_out = file(original_path+"LemLexicon.ttl","w")
    
    lexicon = "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
    
    lexicon += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
    lexicon += "@prefix lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#> .\n"
    lexicon += "@prefix lemon: <http://www.monnet-project.eu/lemon#> .\n"
    lexicon += "@prefix foaf: <http://www.mindswap.org/2003/owl/foaf#> .\n"
    lexicon += "@prefix isocat: <http://www.isocat.org/datcat/> .\n"
    lexicon += "@prefix : <http://sc.cit-ec.uni-bielefeld.de/lexica/automatic/dbpedia#>.\n "
    lexicon += "\t :lexicon a lemon:Lexicon ;\n"
    lexicon += "\t lemon:language \"en\" ;\n"
    
    print "number of lex entries: "+str(len(lemonEntriesHm))
    punkt_counter = 0
    for key in lemonEntriesHm: 
        punkt_counter +=1
        try:
            term = createEntryTerm(key)
            if term != "" :
                string = term +str(punkt_counter)
                if string.endswith(" "):
                    string = string[:-1]
                if re.search("[^a-zA-Z0-9_]",string) == None:
                    try:
#                        string.decode('ascii')
                        string = string.encode("ascii","ignore")
                        if punkt_counter == len(lemonEntriesHm):
                            lexicon += "\t lemon:entry :"+string+" .\n"
                        else:
                            lexicon += "\t lemon:entry :"+string+" ;\n"
                    except:
                        pass
        except:
            #pass
            print "error with entry: "+key

    if lexicon.endswith(";\n"):
        lexicon = lexicon[:-2]
        lexicon += ".\n"
    punkt_counter = 0
    for key in lemonEntriesHm:
        punkt_counter +=1
        try:
            term = createEntryTerm(key)
            if term != "" :
                
                replace_string = term
                if replace_string.endswith(" "):
                    replace_string = replace_string[:-1]
                if re.search("[^a-zA-Z0-9_]",replace_string) == None:
                    try:
#                        replace_string.decode('ascii')
                        replace_string = replace_string.encode("ascii","ignore")
                        string = key.replace(":"+replace_string,":"+replace_string+str(punkt_counter))
                        lexicon+=string+"\n\n"
                    except:
                        pass
        except:
            #pass
            print "error with entry: "+key
    
    f_out.write(lexicon)
    f_out.close()
    
    
   
   
   
def createEntryTerm(entry):
    try:
        compare_item = str(entry).split(";")[0]
        compare_item = compare_item.lower()
        compare_item = compare_item.replace("a lemon:lexicalentry","")
        compare_item = compare_item.replace(":","")
        compare_item = compare_item.replace(" ","")
        compare_item = compare_item.replace("\xc3\xbc","ue")
        compare_item = compare_item.replace("\xc3\xa4","ae")
        compare_item = compare_item.replace("\xc3\x9f","ss")
        compare_item = compare_item.replace("\xc3\xb6","oe")
        return compare_item
    except:
        return entry 
    
    
    ################################################################
    
    
    
def main():
    """
    Main function - does not take any input from command line.
    All settings has to be done in the config.conf
    """
    _init_()
    print "type quit to enter the program"
    parse_flag = False
    path = raw_input("Please enter a path where the Lexicon should be saved:  ")
    while True:
        input = raw_input("Please enter a valid DBpedia URI:  ")
        if input == "quit" or input == "exit":
            print 
            print "Bye Bye!"
            exit(1)
        elif input == "train":
            #run_and_evaluate("Datasets/dbpedia_train_classes_properties.txt","Datasets/dbpedia-train_de.rdf",path,parse_flag)
#            run_and_evaluate("Datasets/dbpedia_train_classes_properties.txt","Datasets/dbpedia_en.rdf",path,parse_flag)
           run_and_evaluate("Datasets/classes_small","Datasets/dbpedia_en.rdf",path,parse_flag)
#             run_and_evaluate("Datasets/test.txt","Datasets/dbpedia_en.rdf",path,parse_flag)
        else:
            start_time= time()
            try:
                run(input,path,parse_flag)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise
                exit(1)
            print "Done after "+str(round(time()-start_time,2))+" seconds"
             
            

    


if __name__ == "__main__":
   main()
    

        
        


