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

def simpleCombineNNP_German(array,x_variable,y_variable):
    print "In German case - only consider 'double names' such as Barack Obama"
    sentence = str(array)
    foundx = False
    foundy = False
    if len(x_variable.split(" "))>1 and len(y_variable.split(" "))>1:
        for i in range(0,len(array)-1):
            tmp = array[i]
            tmp1 = array[i+1]
            x = x_variable.split(" ")
            y = y_variable.split(" ")
            if tmp[0] in x[0] and  tmp1[0] in x[1]:
                toReplace = "('"+tmp[0]+"', '"+tmp[1]+"'), ('"+tmp1[0]+"', '"+tmp1[1]+"')"
                replaceWith = "('"+tmp[0]+tmp1[0]+"', 'NE')"
                sentence = sentence.replace(toReplace,replaceWith)
                foundx = True
                print ("sentence after x",sentence)
                print ("foundx",foundx)
                
            if tmp[0] in y[0] and  tmp1[0] in y[1]:
                toReplace = "('"+tmp[0]+"', '"+tmp[1]+"'), ('"+tmp1[0]+"', '"+tmp1[1]+"')"
                replaceWith = "('"+tmp[0]+tmp1[0]+"', 'NE')"
                sentence = sentence.replace(toReplace,replaceWith)
                foundy = True
                print ("sentence after y",sentence)
                print ("foundy",foundy)
                
                
        if foundx == True and foundy == True:
            print ("final sentence",sentence)
            return eval(sentence),True,True
        else:
            return array,False,False
            
            
    else:
        return array,False , False
    
    
    
def simpleCombineNNP_Spanish(array,x_variable,y_variable):
    print "In Spanish case"
    sentence = str(array)
    foundx = False
    foundy = False
    print ("x_variable",x_variable)
    print ("y_variable",y_variable)
    if len(x_variable.split(" "))>1 and len(y_variable.split(" "))>1:
        for i in range(0,len(array)-1):
            tmp = array[i]
            tmp1 = array[i+1]
            x = x_variable.split(" ")
            y = y_variable.split(" ")
            if tmp[0] in x[0] and  tmp1[0] in x[1]:
                toReplace = "('"+tmp[0]+"', '"+tmp[1]+"'), ('"+tmp1[0]+"', '"+tmp1[1]+"')"
                replaceWith = "('"+tmp[0]+tmp1[0]+"', 'Propio')"
                sentence = sentence.replace(toReplace,replaceWith)
                foundx = True
                print ("sentence after x",sentence)
                print ("foundx",foundx)
                
            if tmp[0] in y[0] and  tmp1[0] in y[1]:
                toReplace = "('"+tmp[0]+"', '"+tmp[1]+"'), ('"+tmp1[0]+"', '"+tmp1[1]+"')"
                replaceWith = "('"+tmp[0]+tmp1[0]+"', 'Propio')"
                sentence = sentence.replace(toReplace,replaceWith)
                foundy = True
                print ("sentence after y",sentence)
                print ("foundy",foundy)
                
                
        if foundx == True and foundy == True:
            print ("final sentence",sentence)
            return eval(sentence),True,True
        else:
            return array,False,False
            
            
    else:
        return array,False , False
    
def combineNNP(array,x_variable,y_variable,language):
    print ("in combine NNP",language)
    if language=="German":
        return simpleCombineNNP_German(array,x_variable,y_variable)
    elif language=="Spanish":
        return simpleCombineNNP_Spanish(array,x_variable,y_variable)
    
    
    # 1. Combine all NNP
    cluster = []
    foundx = False
    foundy = False
    tmp = []
    counter = 0
    for i in range(0,len(array)-1):
#         if "CD" in array[i][1]:
#             counter += 1
        if ("NNP" in array[i][1] or "NNPS" in array[i][1] or "CD" in array[i][1]) and counter < 2:
            tmp.append(i)
        else:
            if len(tmp) > 1 :
#                 print ("cluster", tmp)
                cluster.append(tmp)
                tmp = []
            else: 
                tmp = []
            if counter >= 2:
                tmp.append(i)
                counter = 0
            else:
                counter = 0
                
    new_array = []
    for x in cluster:
        string = ""
        for i in x:
            string += array[i][0]+" "
        string = string[:-1]
        if x_variable.lower() in string.lower():
            string = ((x_variable.lower()).replace(" ","")).capitalize()
            foundx = True
        if y_variable.lower() in string.lower():
            string = ((y_variable.lower()).replace(" ","")).capitalize()
            foundy = True
#         string = (string.replace(" ",""),'NNP')
        string = (string,'NNP')
        x.append(string)
        
    hm = {}
    counter = 0
    for x in cluster:
        for i in x[:-1]:
            hm[i] = counter
        counter += 1
    
    tmp = True
    for i in range(0,len(array)-1):
        if hm.has_key(i):
            if tmp == True:
                t_a = cluster[hm[i]]
                t = t_a[len(t_a)-1:]
                new_array.append(t[0])
                tmp = False
        else:
            new_array.append(array[i])
            tmp = True
    
    if foundx == False or foundy == False:
        tmp_array = []

        
        for e in new_array:
            
            if e[0] == y_variable and foundy == False:
                tmp_array.append((y_variable.replace(" ","").capitalize(),"NNP"))
                foundy = True
            elif e[0] == x_variable and foundx == False:
                tmp_array.append((x_variable.replace(" ","").capitalize(),"NNP"))
                foundx = True
            else:
                tmp_array.append((e[0],e[1]))
        return tmp_array, foundx, foundy
    else:
        return new_array, foundx, foundy
        

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
    language = config.get('system_language', 'language')
    procentOfDataset = 100
    overall_sentences = 0
    special = False
#     if config.get("index","advancedEnglishIndex") == "True" and config.get('system_language', 'language') == "English":
#         special = True
# #    else:
# #        special = False
    print ("special",str(special))
    print ("config.get(\"index","advancedEnglishIndex\")",config.get("index","advancedEnglishIndex"))
    print ("config.get('system_language', 'language')",config.get('system_language', 'language'))
        
    ###############
    ##
    ## TODO: After testing, make this user friendly
    ##
    ###############
    if special == True:
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
    tolerance_procent = 1
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
            if x != y and x.lower() not in y.lower() and y.lower() not in x.lower():
                if special == True:
                    result= index.search(key_list,special)

                    print
                else:

                    #print ("search term",term)
                    result= index.search(term,special)
                    #print "len result: "+str(len(result))
                    overall_sentences += len(result)

            for line_array in result:
                found_x = False
                found_y = False
                print line_array,x,y,language
                line_array,found_x,found_y = combineNNP(line_array,x,y,language)
#                 print line_array
                line = ""
                for e in line_array:
                    line += e[0]+" " 
                        
                if found_x == True and found_y == True:
                    #Use each line only for one x-y pair
                    if line not in hm:
                        hm[line]=[x,y,line_array]
            
        except Exception:
            print "Unexpected error on lookup terms in lookupSortAndParse:", sys.exc_info()[0]
            #print ("Error in finding term: "+str(item))
     
    print "found "+str(overall_sentences)+" sentences"
    print "found "+str(len(hm))+" combination of pairs and sentences"

        
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
                not_in_index.append([key,tmp[0],tmp[1],tmp[2]])
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
        parse_list.append(item[3])
 
    """
    Path, where MaltParser saves the sentences
    """
    sfile="/tmp/tmp.txt"
    
    sentence_value = 20000
    """
    parses always x sentences at once.
    For other languages, here it has to be checked, which language is given and which parser has to be used.
    """    
    tolerance = 0.0
    if len(parse_list)>tolerance:
#        raw_input(str(sentence_value))
        if len(parse_list) < sentence_value:
            print ("in case 1")
#            m_parser.parses_list_of_sentences(parse_list, sfile)
            parser.parse(parse_list, sfile)
            parsed_sentences = load_file_return_list_of_sentences(sfile)
            to_add = []
            print len(parsed_sentences)
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
            

        
        
        
        


