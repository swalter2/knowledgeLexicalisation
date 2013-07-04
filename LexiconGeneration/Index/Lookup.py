import sys, os
from Parser.Parser import Sentence_Parser

import IndexUtils, ConfigParser

def clean_sentence(sentence):
        
    sentence = sentence.replace(","," ")
    sentence = sentence.replace("."," ")
    sentence = sentence.replace("!"," ")
    sentence = sentence.replace("?"," ")
    sentence = sentence.replace("("," ")
    sentence = sentence.replace(")"," ")
    sentence = sentence.replace("_"," ")
    sentence = sentence.replace("-"," ")
    sentence = sentence.replace(":"," ")
        
    while "  " in sentence:
        sentence = sentence.replace("  "," ")
            
    if sentence.endswith(" "):
        sentence = sentence[:len(sentence)-1]
            
    return sentence
  
def add_sentenceList_to_Index(sentenceList,hm, live_index):
    """
    Adds sentences to a given index, with parsed sentences.
    Not uses in the moment.
    """
    for sentence in sentenceList:
        sentence=sentence.replace("\t"," ")
        sentence=sentence.replace("\n"," ")
        live_index.update_index_withLine(sentence)
        print "added: "+sentence

      
    
def check_sentenceList_in_Index(list, live_index):
    """
    Checks a given list of sentences, if they exist in the Index with the parsed sentences, or not.
    Sentences which are not in the Index, are returned in an array.
    """
    num_of_errors = 0
    return_list=[]
    counter=0
    for line in list:
        line = clean_sentence(line)
        line = line[:len(line)-2]
        counter+=1
        try:
            if live_index.does_line_exist(line)==False:
                return_list.append(line)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print "check_sentenceList_in_Index with line: "+line+" \n\n"
            num_of_errors+=1

    return return_list 

def load_file_return_list_of_sentences(file_path):
    """
    Loads a given file and returns sentences as array.
    """
    f=file(file_path,"r")
    sentence_list=[]
    sentence=""
    for line in f:
        if line=="\n":
            sentence_list.append(sentence)
            sentence=""
        else:
            sentence+=line+" "
    f.close()
    return sentence_list



def lookupSortAndParse(term_list,index,live_index, flag,uri):
    """
    Retrieves a set of Entities, the corresponding DBpedia URI, the index with the English corpus and the index of the parsed sentences.
    First all sentences are retrieved from the corpus index, where the sentences match to a entity pair.
    In the next step, each entity is identified in the sentences and the words are combined. E.g. out of Barack Obama the term BarackObama is created in the sentence.
    In the third step, each sentence is matches to the index with the parsed sentences. If the sentences is already parsed, nothing happens, if the sentence is not parsed,
    it will be parsed using the MaltParser and will be added to the index with the parsed sentences.
    This function is ONLY called, if new sentences shall be add to the index, otherwise this function - which need a lot of time - is ignored and the sentences are directly extracted
    from the parsed sentence index and not from the given plain text corpus
    """
    config = ConfigParser.ConfigParser()
    config.read('config.conf')
#    procentOfDataset = config.getint("entries", "ProcentOfCorpus")
    procentOfDataset = 100

    special = False
    if config.get("index","advancedEnglishIndex") == "True" and config.get('system_language', 'language') == "English":
        special = True
#    else:
#        special = False
    print ("special",str(special))
    print ("config.get(\"index","advancedEnglishIndex\")",config.get("index","advancedEnglishIndex"))
    print ("config.get('system_language', 'language')",config.get('system_language', 'language'))
        
    ###############
    ##
    ## TODO: After testing, make this user friendly
    ##
    ###############
    f_in = open("/home/swalter/keystore_out","r")
    hm_key = {}
    for line in f_in:
        line = line.replace("\n","")
        tmp = line.split("\t")
        hm_key[tmp[1].lower()]=tmp[0]
    f_in.close()
    print "keystore created"
    ##############
        
    parser = Sentence_Parser()
    not_in_index = []
    hm = {}
    tolerance_procent = 15
    tolerance = 0
    for item in term_list:
        try:
            term = item[0]
            x = item[1]
            y = item[2]
            x = x.encode("ascii","ignore")
            y = y.encode("ascii","ignore")

            key_list = []
###############################################
###############################################
#
#Create subset of keys
            if special == True:
                print "create subset of keys"
                if hm_key.has_key(x.lower()):
                    key_list.append(hm_key[x.lower()])
                if hm_key.has_key(y.lower()):
                    key_list.append(hm_key[y.lower()])
                print ("key_list",key_list)
                if len(key_list) == 0:
                    #only to make sure, that search isnt started
                    x = "a"
                    y = "a"
###############################################
###############################################

            result = []
            if x != y:
                if special == True:
                    print "start special search"
                    result= index.search(key_list,special)
                    print "returned "+str(len(result))+" sentences for special search"
                    print
                else:
                    result= index.search(term,special)
                tmp = result
                result = []
                for t in tmp:
                    #To Deal with German Umlaute
                    t = t.replace("\xc3\xa4","ae")
                    t = t.replace("\xc3\x9f","ss")
                    t = t.replace("\xc3\xbc","ue")
                    t = t.replace("\xc3\xb6","oe")
                    t = t.replace("\xe2\x80\x9e","\"")
                    t = t.replace("\xe2\x80\x9c","\"")
                    t = t.replace("\xc3\xba","u")
                    t = t.replace("\xe2\x80\x9e","\"")
                    t = t.replace("\xe2\x80\x99","'")
                    t = t.replace("\xe2\x80\x93","-")
                    t = t.replace("\xe2\x80\x94","-")
                    t = t.replace("\xe2\x80\x95","-")
                    result.append(t)
                        
#            print str(len(result))+" number of sentences found in Corpus"
            for line in result:
                found_x = True
                found_y = True
                replacementX = x.replace(" ","")
                
                if x in line:
                    line = line.replace(x,replacementX.capitalize())
                else:
                    found_x = False
                
                replacementY = y.replace(" ","")
                
                if y in line: 
                    line = line.replace(y,replacementY.capitalize())
                    
                else:
                    found_y = False

                if found_x == True and found_y == False:
                    if " " in y:
                        searchY = y.split(" ")[0]
                        if searchY in line:
                            if searchY != x:
                                line = line.replace(" "+searchY+" ",replacementY.capitalize())
                                found_y = True
                            else:
                                if " he " in line or " she " in line or " it " in line:
                                    line = line.replace(" he ",replacementY.capitalize())
                                    line = line.replace(" she ",replacementY.capitalize())
                                    line = line.replace(" it ",replacementY.capitalize())
                                    found_y = True  
                if found_x == False and found_y == True:
                    if " " in x:
                        searchX = x.split(" ")[0]
                        if searchX in line:
                            if searchX != y:
                                line = line.replace(" "+searchX+" ",replacementX.capitalize())
                                found_x = True
                            else:
                                if " he " in line or " she " in line or " it " in line:
                                  line = line.replace(" he ",replacementX.capitalize())
                                  line = line.replace(" she ",replacementX.capitalize())
                                  line = line.replace(" it ",replacementX.capitalize())
                                  found_x = True  
                        
                if found_x == True and found_y == True:
                    #Use each line only for one x-y pair
                    if line not in hm:
                        hm[line]=[x,y]
            
        except Exception:
            print "Unexpected error on lookup terms in lookupSortAndParse:", sys.exc_info()[0]
            #print ("Error in finding term: "+str(item))
     
    print "found "+str(len(hm))+" combination of pairs and sentences"
    #German Umlaute
#    for key in hm:
#        print (key.replace("\xc3\xa4","ae").replace("\xc3\x9f","ss").replace("\xc3\xbc","ue"),hm[key])
#    print
        
    if len(hm) > 0:
        tolerance = (len(hm)+0.0)/100*tolerance_procent
        
    parse_list = []
    
    ######################################
    #
    #Before parsing, check, if the sentences are already parsed or not!
    #
    ######################################
    true_counter = 0
    for key in hm:
        try:
            tmp = hm[key]
            inIndex = live_index.does_line_exist(key,str(tmp[0]),str(tmp[1]))
            if inIndex == False:
                not_in_index.append([key,tmp[0],tmp[1]])
            else:
                true_counter += 1
        except:
            print "Error"
            print "Unexpected error:", sys.exc_info()[0]
            print
    print "created List with not existing sentences"
    print "Number of not parsed sentences: "+str(len(not_in_index))
    hm = {}

    for item in not_in_index:
        parse_list.append(item[0])
 
    """
    Path, where MaltParser saves the sentences
    """
    sfile="/tmp/tmp.txt"
    
    sentence_value = 10000
    """
    parses always x sentences at once.
    For other languages, here it has to be checked, which language is given and which parser has to be used.
    """    
    if len(parse_list)>tolerance:
#        raw_input(str(sentence_value))
        if len(parse_list) < sentence_value:
            print ("in case 1")
#            m_parser.parses_list_of_sentences(parse_list, sfile)
            parser.parse(parse_list, sfile)
            parsed_sentences = load_file_return_list_of_sentences(sfile)
            to_add = []
            for i in range(0,len(parsed_sentences)):
                tmp = not_in_index[i]
                to_add.append([parsed_sentences[i],tmp[1],tmp[2],uri])
            live_index.update_index_withLineArray(to_add)
            parsed_sentences = []
            to_add = []
            
            
        elif len(parse_list) > sentence_value:
            print ("in case 2")
            print ("sentence value",sentence_value)
            p_counter = 0
            new_list = []
            for s in parse_list:
                p_counter += 1
                new_list.append(s)
                if (p_counter%sentence_value == 0):
                    parser.parse(new_list, sfile)
                    new_list = []
                    parsed_sentences = load_file_return_list_of_sentences(sfile)
                    to_add = []
                    for i in range(0,len(parsed_sentences)):
                        tmp = not_in_index[i+p_counter-sentence_value]
                        to_add.append([parsed_sentences[i],tmp[1],tmp[2],uri])
                        
                    live_index.update_index_withLineArray(to_add)
                    parsed_sentences = []
                    to_add = []

            parser.parse(new_list, sfile)
            new_list = []
            parsed_sentences = load_file_return_list_of_sentences(sfile)
            to_add = []
            offset = p_counter%sentence_value
            for i in range(0,len(parsed_sentences)):
                
                tmp = not_in_index[i+p_counter-offset]
                to_add.append([parsed_sentences[i],tmp[1],tmp[2],uri])

            live_index.update_index_withLineArray(to_add)
            parsed_sentences = []
            to_add = []

            parsed_sentences = []
            

        
        
        
        


