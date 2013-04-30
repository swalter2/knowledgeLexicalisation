#!/usr/bin/python
import os, re, sys, ConfigParser
from time import time
from Util import Sparql
from LexiconGeneration import LexiconGenerator
from LexiconGeneration import Approach1

from LexiconGeneration.Parser import MaltParser
from LexiconGeneration.Index import Index, LiveIndex, AnchorIndex

m_parser = None
index = None
parsed_sentence_index = None
anchor_index = None
    
    
        
        
def _init_():
    """
    Initialisation of the Index and the Parser
    """
    print "start initialisation"
    global m_parser
    global index
    global parsed_sentence_index

    
    config = ConfigParser.ConfigParser()
    config.read('config.conf')


    working_Dir = config.get('parser', 'working_Dir')
    
    
    
    #pretrained model in format mco
    mco_File = config.get('parser', 'mco_file')
    
    maltparser_Jar = config.get('parser', 'maltparser_Jar')
    
    path_to_index = config.get('index', 'wikipedia_index');

    
    
    #Set true if you want to use the official Version from NLTK or False if you want to use the Malt.py in this Folder
    official_Malt_Parser=config.get('parser', 'official_Malt_Parser');
    os.environ["MALTPARSERHOME"] = config.get('parser', 'parser_dir')
        
    m_parser=MaltParser.Parser(working_Dir, mco_File, maltparser_Jar,official_Malt_Parser)
    index = Index.LuceneIndex(path_to_index)
    
    
    
    parsed_sentence_index = LiveIndex.LiveIndex(config.get('index', 'wikipedia_live_index'))
    
    global anchor_index
    anchor_index = AnchorIndex.LuceneIndex(config.get('index', 'anchor_index'))
    
    print "initialisation done"
    
    
    




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
   #web_string += "<p><a href=\""+"../../LemonLexiconDbpedia/lemon_lexica.rdf\"> LemonLexica </a></p>"
   
   
   
   
    

    string =""
    tmp_hm = {}
   
    if sparql.askClassProperty(uri) == True:
       entryArray = LexiconGenerator.createClassEntry(uri)
       for entry in entryArray:
           lemonEntriesHm[entry] = ""
    else:
        string, tmp_hm = Approach1.creatingLexiconEntry_for_singleURI(False, uri, parse_flag, path, index,parsed_sentence_index,m_parser,anchor_index)
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
   
    #web_array.append(string)
    f=file(path+"index.html","w")
    f.write(web_string)
    f.close()
   
    
    #__destroy__() 
    print "\n\n DONE"
    
    
    
    
def write_lexicon(original_path,lemonEntriesHm):
    """
    Writes the Lemonentries to a file on a given path
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
                        string.decode('ascii')
                        if punkt_counter == len(lemonEntriesHm):
                            lexicon += "\t lemon:entry :"+string+" .\n"
                        else:
                            lexicon += "\t lemon:entry :"+string+" ;\n"
                    except:
                        pass
        except:
            #pass
            print "error with entry: "+key
            #raw_input("wait")

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
                        replace_string.decode('ascii')
                        string = key.replace(":"+replace_string,":"+replace_string+str(punkt_counter))
                        lexicon+=string+"\n\n"
                    except:
                        pass
        except:
            #pass
            print "error with entry: "+key
            #raw_input("wait")
    
    f_out.write(lexicon)
    f_out.close()
    
    
   
   
   
def createEntryTerm(entry):
    try:
        #print str(entry)
        compare_item = str(entry).split(";")[0]
        compare_item = compare_item.lower()
        compare_item = compare_item.replace("a lemon:lexicalentry","")
        compare_item = compare_item.replace(":","")
        compare_item = compare_item.replace(" ","")
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
    path = raw_input("Please enter a path where the Lexicon should be saved.")
    while True:
        input = raw_input("Please enter a valid DBpedia URI:")
        if input == "quit":
            print 
            print "Bye Bye!"
            exit(1)
        else:
            start_time= time()
            try:
                run(input,path,parse_flag)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise
                exit(1)
            print "Done after "+str(round(time()-start_time,2))+" seconds"
            

    


main()
    

        
        


