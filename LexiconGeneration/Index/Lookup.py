import sys, os
#lib_path = os.path.abspath('Index')
#sys.path.append(lib_path)

import IndexUtils, ConfigParser

def clean_sentence1(sentence):
        
    sentence = sentence.replace(","," ")
    sentence = sentence.replace("."," ")
    sentence = sentence.replace("!"," ")
    sentence = sentence.replace("?"," ")
    sentence = sentence.replace("("," ")
    sentence = sentence.replace(")"," ")
    sentence = sentence.replace("_"," ")
    sentence = sentence.replace("-"," ")
    sentence = sentence.replace(":"," ")
    #sentence = sentence.repalce("\""," ")
        
    while "  " in sentence:
        sentence = sentence.replace("  "," ")
            
    if sentence.endswith(" "):
        sentence = sentence[:len(sentence)-1]
            
    return sentence
  
def add_sentenceList_to_Index(sentenceList,hm, live_index):
    for sentence in sentenceList:
        sentence=sentence.replace("\t"," ")
        sentence=sentence.replace("\n"," ")
        live_index.update_index_withLine(sentence)
        print "added: "+sentence

      
    
def check_sentenceList_in_Index(list, live_index):
    print "in check_sentenceList_in_Index"
    'get a list with sentences!!!'
    'returns a list of sentences, which has to be parsed - in NL and not in the new data type'
    num_of_errors = 0
    return_list=[]
    counter=0
    for line in list:
        line = clean_sentence1(line)
        #TODO: Why?
        line = line[:len(line)-2]
        #print line
        counter+=1
        #print str(counter)
        try:
            if live_index.does_line_exist(line)==False:
                return_list.append(line)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print "check_sentenceList_in_Index with line: "+line+" \n\n"
            num_of_errors+=1

    return return_list 

def load_file_return_list_of_sentences(file_path):
    
    #load_Ontology_Classes("/home/swalter/Downloads/Ontology/dbpedia_3.6.owl")
    #load_Properties("/home/swalter/Downloads/Ontology/dbpedia_3.6.owl")
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



def lookupSortAndParse(term_list,index,live_index, m_parser, flag,uri):
    config = ConfigParser.ConfigParser()
    config.read('settings.ini')
    procentOfDataset = config.getint("entries", "ProcentOfCorpus")

    not_in_index = []
#    sentence_array = []
    hm = {}
    tolerance_procent = 15
    tolerance = 0
    for item in term_list:
        try:
            term = item[0]
            x = item[1]
            #x = x.lower()
            y = item[2]
            #y = y.lower()
            result = []
            if x != y:
                #rank is not important any more
                #print "term: "+str(term)
                result= index.search(term,1)
                
            
            for line in result:
                #line = line.lower()
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
                        
                if found_x == True and found_y == True:
                    #Take each line only for one x-y pair
                    if line in hm:
#                        tmp_hm = hm[line]
#                        tmp_hm[x+"###"+y]=""
                        #hm[line] = [x,y]
                        pass
                    else:
#                        tmp_hm = {}
#                        tmp_hm[x+"###"+y]=""
                        hm[line]=[x,y]
            
        except Exception:
            print "Unexpected error:", sys.exc_info()[0]
            print ("Error in finding term: "+str(item))
     
    print "found "+str(len(hm))+" combination of pairs and sentences"
#            #pass
#    if len(hm) >200000:
#        print len(hm)
#        #raw_input("more than 200000 sentences")
#        array_t = hm.keys()[:200000]
#        hm_new = {}
#        for item in array_t:
#            hm_new[item]=hm[item]
#        hm.clear()
#        hm = hm_new.copy()
#        hm_new.clear()
        
    if len(hm) > 0:
        tolerance = (len(hm)+0.0)/100*tolerance_procent
    
#    number_of_sentences = len(hm)
#    numberOfSentencesFromDataset = int((number_of_sentences/100.0*procentOfDataset))
#    counter = 0
#    for key in hm:
#        counter += 1
#        if counter < numberOfSentencesFromDataset:
#            tmp_array = []
#            tmp_array.append(key)
#            for entry in hm[key]:
#                tmp_array.append(entry)
#            sentence_array.append(tmp_array)
        
    parse_list = []
    
    ######################################
    #
    #Before parsing, check, if the sentences are already parsed or not!
    #
    ######################################
    #t2 = time()
    true_counter = 0
    for key in hm:
        try:
            tmp = hm[key]
            inIndex = live_index.does_line_exist(key,str(tmp[0]),str(tmp[1]))
            if inIndex == False:
                not_in_index.append([key,tmp[0],tmp[1]])
#                print key
#                print
            else:
                true_counter += 1
        except:
            print "Error"
            print "Unexpected error:", sys.exc_info()[0]
            print
    print "created List with not existing sentences"
    print len(not_in_index)
    print "len(hm): "+str(len(hm))
    print "true_counter: "+str(true_counter)
    hm = {}

    for item in not_in_index:
        parse_list.append(item[0])
 
    sfile="/tmp/tmp.txt"
    #parse all sentences at once
    
    ##################################
    #
    #Only parse, if more than number of procentOfDataset sentences in the list.
    #
    ##################################


    
    
    if len(parse_list)>tolerance:
        if len(parse_list) < 10000:
            m_parser.parses_list_of_sentences(parse_list, sfile)
            parsed_sentences = load_file_return_list_of_sentences(sfile)
            to_add = []
            for i in range(0,len(parsed_sentences)):
                tmp = not_in_index[i]
                to_add.append([parsed_sentences[i],tmp[1],tmp[2],uri])
            live_index.update_index_withLineArray(to_add)
            parsed_sentences = []
            to_add = []
            
            
        else:
            p_counter = 0
            new_list = []
            for s in parse_list:
                p_counter += 1
                new_list.append(s)
                if (p_counter%10000 == 0):
                    m_parser.parses_list_of_sentences(new_list, sfile)
                    new_list = []
                    parsed_sentences = load_file_return_list_of_sentences(sfile)
                    to_add = []
                    for i in range(0,len(parsed_sentences)):
                        tmp = not_in_index[i+p_counter-10000]
                        to_add.append([parsed_sentences[i],tmp[1],tmp[2],uri])
#                        print parsed_sentences[i]
#                        print "x: "+tmp[1]
#                        print "y: "+tmp[2]
                        #live_index.update_index_withLine(parsed_sentences[i],tmp[1],tmp[2])
                    live_index.update_index_withLineArray(to_add)
                    parsed_sentences = []
                    to_add = []
#                        print len(parsed_sentences[i])
#                        live_index.update_index_withLine(parsed_sentences[i])
                    #use p_counter as offset!
                    
                    
#                    for s_t in parsed_sentences_t:
#                        parsed_sentences.append(s_t)
#                    new_list = []
#                    parsed_sentences_t = []
#                    p_counter = 0
            m_parser.parses_list_of_sentences(new_list, sfile)
            new_list = []
            parsed_sentences = load_file_return_list_of_sentences(sfile)
            to_add = []
            offset = p_counter%10000
            for i in range(0,len(parsed_sentences)):
                
                tmp = not_in_index[i+p_counter-offset]
                to_add.append([parsed_sentences[i],tmp[1],tmp[2],uri])
#                        print parsed_sentences[i]
#                        print "x: "+tmp[1]
#                        print "y: "+tmp[2]
                #live_index.update_index_withLine(parsed_sentences[i],tmp[1],tmp[2])
            live_index.update_index_withLineArray(to_add)
            parsed_sentences = []
            to_add = []
#            for s_t in parsed_sentences_t:
#                parsed_sentences.append(s_t)
#            new_list = []
            parsed_sentences = []
            
#    parse_list = []
#            
#            
#    add_counter = 0
#    error_counter = 0
#            
#    add_counter, error_counter = live_index.update_index_withLineArray(parsed_sentences)
#
#    #replace not parsed sentences with parsed sentences
#    for x in range(0,len(parsed_sentences)):
#        try:
#            sentence = parsed_sentences[x]
#            sentence = sentence.replace("\t"," ")
#            sentence = sentence.replace("\n"," ")
#        
#            if sentence[len(sentence)-2:] == "  ":
#                sentence = sentence[:len(sentence)-2]
#            
#            not_in_index[x][0] = IndexUtils.sentence_wrapper(sentence)
#        except:
#            pass
#    parsed_sentences = []

        
        
        
        


#def lookupSortAndParse(term_list,index,live_index, m_parser, flag):
#    config = ConfigParser.ConfigParser()
#    config.read('settings.ini')
#    procentOfDataset = config.getint("entries", "ProcentOfCorpus")
#    
#    in_index = []
#    not_in_index = []
#    sentence_array = []
#    hm = {}
#    tolerance_procent = 15
#    tolerance = 0
#    for item in term_list:
#        try:
#            term = item[0]
#            x = item[1]
#            #x = x.lower()
#            y = item[2]
#            #y = y.lower()
#            result = []
#            if x != y:
#                result= index.search(term,2)
#                
#            
#            for line in result:
#                #line = line.lower()
#                found_x = True
#                found_y = True
#                replacementX = x.replace(" ","")
#                
#                
#                if x in line:
#                    line = line.replace(x,replacementX.capitalize())
#                else:
#                    found_x = False
#                
#                replacementY = y.replace(" ","")
#                
#                if y in line: 
#                    line = line.replace(y,replacementY.capitalize())
#                    
#                else:
#                    found_y = False
#                
#                #with new terms, always only look for a direct match!
#                foundy = True
#                foundx = True
#                
#                if found_x == False and " " in x:
#                    tmp = x.split(" ")
#                    if len(tmp) == 2:
#                        if tmp[1]+" "+tmp[0] in line:
#                            #print line
#                            line = line.replace(tmp[1]+" "+tmp[0],replacementX.capitalize())
#                            found_x = True
#                            
#                    for t in tmp:
#                        if " "+t+" " in line and len(t)>2:
#                            line = line.replace(" "+t+" "," "+replacementX.capitalize()+" ")
#                            found_x = True
#                            break
#                        #But what happens at end of sentences or before a ,???
#                        if (line.replace(",","").replace(".","")).endswith(t):
#                            line = line.replace(" "+t," "+replacementX.capitalize())
#                            found_x = True
#                            break
#                
#                        
#                if found_y == False and " " in y:
#                    tmp = y.split(" ")
#                    
#                    #neva river is the original term, but can also be river neva
#                    if len(tmp) == 2:
#                        if tmp[1]+" "+tmp[0] in line:
#                            #print line
#                            line = line.replace(tmp[1]+" "+tmp[0],replacementY.capitalize())
#                            found_y = True
#
#                        
#                    for t in tmp:
#                        if " "+t+" " in line and len(t)>2:
#                            line = line.replace(" "+t+" "," "+replacementY.capitalize()+" ")
#                            found_y = True
#                            break
#                            #But what happens at end of sentences or before a ,???
#                        if (line.replace(",","").replace(".","")).endswith(t):
#                            line = line.replace(" "+t," "+replacementY.capitalize())
#                            found_y = True
#                            break
#                            
#                        
#                if found_x == True and found_y == True:
#                    if line in hm:
#                        tmp_hm = hm[line]
#                        tmp_hm[x+"###"+y]=""
#                        hm[line] = tmp_hm
#                    else:
#                        tmp_hm = {}
#                        tmp_hm[x+"###"+y]=""
#                        hm[line]=tmp_hm
# #bis hier sind die saetze richtig...
#        except Exception:
#            print "Unexpected error:", sys.exc_info()[0]
#            print ("Error in finding term: "+str(item))
#     
#            #pass
#    if len(hm) >200000:
#        print len(hm)
#        #raw_input("more than 200000 sentences")
#        array_t = hm.keys()[:200000]
#        hm_new = {}
#        for item in array_t:
#            hm_new[item]=hm[item]
#        hm.clear()
#        hm = hm_new.copy()
#        hm_new.clear()
#        
#    if len(hm) > 0:
#        tolerance = (len(hm)+0.0)/100*tolerance_procent
#    
#    number_of_sentences = len(hm)
#    numberOfSentencesFromDataset = int((number_of_sentences/100.0*procentOfDataset))
#    counter = 0
#    for key in hm:
#        counter += 1
#        if counter < numberOfSentencesFromDataset:
#            tmp_array = []
#            tmp_array.append(key)
#            for entry in hm[key]:
#                tmp_array.append(entry)
#            sentence_array.append(tmp_array)
#        
#    parse_list = []
#    
#    ######################################
#    #
#    #Before parsing, check, if the sentences are already parsed or not!
#    #
#    ######################################
#    #t2 = time()
#    for item in sentence_array:
#        try:
#            inIndex = live_index.does_line_exist(item[0])
#            if inIndex == False:
#                not_in_index.append(item)
#            elif inIndex == True:
#                #get line from Index!
#                try:
#                    tmp_item = item
#                    tmp_item[0] = live_index.search(item[0])[0]
#                    in_index.append(tmp_item)
#                    #in_index.append(item)
#                except:
#                    pass
#        except:
#            pass
#    sentence_array = []
#    #flag == True means, that new sentences has to be parsed and added to the index, false means, all found sentences are returned
#    if flag == False:
#        not_in_index = []
#        hm.clear()
#        return in_index
#    
#    for item in not_in_index:
#        parse_list.append(item[0])
# 
#    sfile="/tmp/tmp.txt"
#    #parse all sentences at once
#    
#    ##################################
#    #
#    #Only parse, if more than number of procentOfDataset sentences in the list.
#    #
#    ##################################
#    parsed_sentences = []
#
#    
#    
#    if len(parse_list)>tolerance:
#        if len(parse_list) < 10000:
#            m_parser.parses_list_of_sentences(parse_list, sfile)
#            parsed_sentences = load_file_return_list_of_sentences(sfile)
#            
#        else:
#            p_counter = 0
#            new_list = []
#            for s in parse_list:
#                p_counter += 1
#                new_list.append(s)
#                if (p_counter%10000 == 0):
#                    m_parser.parses_list_of_sentences(new_list, sfile)
#                    parsed_sentences_t = load_file_return_list_of_sentences(sfile)
#                    for s_t in parsed_sentences_t:
#                        parsed_sentences.append(s_t)
#                    new_list = []
#                    parsed_sentences_t = []
#                    p_counter = 0
#            m_parser.parses_list_of_sentences(new_list, sfile)
#            parsed_sentences_t = load_file_return_list_of_sentences(sfile)
#            for s_t in parsed_sentences_t:
#                parsed_sentences.append(s_t)
#            new_list = []
#            parsed_sentences_t = []
#            
#    parse_list = []
#            
#            
#    add_counter = 0
#    error_counter = 0
#    #now add new lines to Index!
#    #for item in parsed_sentences:
#    #    sentence = item
#    #    sentence=sentence.replace("\t"," ")
#    #    sentence=sentence.replace("\n"," ")
#    #    try:
#    #        live_index.update_index_withLine(sentence)
#    #        add_counter += 1
#    #        #print "added"
#    #    except:
#    #        error_counter += 1
#    #        print "error"
#    #        print
#            
#    add_counter, error_counter = live_index.update_index_withLineArray(parsed_sentences)
#
#    #replace not parsed sentences with parsed sentences
#    for x in range(0,len(parsed_sentences)):
#        try:
#            sentence = parsed_sentences[x]
#            sentence = sentence.replace("\t"," ")
#            sentence = sentence.replace("\n"," ")
#        
#            if sentence[len(sentence)-2:] == "  ":
#                sentence = sentence[:len(sentence)-2]
#            
#            not_in_index[x][0] = IndexUtils.sentence_wrapper(sentence)
#        except:
#            pass
#    parsed_sentences = []
#    #now add parsed sentecnes and x/y to the in_index array and return array
#    for item in not_in_index:
#        in_index.append(item)
#    
#    #Delete arrays.
#    not_in_index = []
#    hm.clear()
#    print str(error_counter)+" could not be added to Index!!!"
#    return in_index
#        
#        
        

#def lookup(term, flag, index, m_parser, live_index):
#    'returns all sentences in an live_index'
#    
#    parse_flag = False
#    #print "Term :"+term
#    
#    try:
#        return live_index.search(term)
#    except Exception:
#        print "Unexpected error:", sys.exc_info()[0]
#        print "in lookup"
#        raw_input("Enter Key to continue")
#    
#    
#def lookup_in_sentence_with_entityrecognition(sentence, index_after_ER, er_index):
#    #TODO: remove return later!
#    return sentence
#    global global_test_counter
#    global global_test_counter_sentences
#    'the input sentence is already the PARSED index'
#    #print "in lookup_in_sentence_with_entityrecognition"
#    
#    search_term = ""
#    try:
#        for item in sentence.split("  "):
#            if " " in item:
#                search_term += item.split(" ")[1]+" "
#    except Exception:
#        print "Unexpected error:", sys.exc_info()[0]
#        print "error in function lookup_in_sentence_with_entityrecognition"
#        #print "error in "+search_term+"\n\n"
#    #look, if sentence already exists
#    if index_after_ER.does_line_exist(search_term) :
#        line = er_index.regognise_e(sentence)
#        
#        return line
#    else:
#        line = None
#        try:
#            line = er_index.regognise_e(sentence)
#            global_test_counter +=1
#            global_test_counter_sentences += sentence+"\n\n"
#        except Exception:
#            print "Unexpected error:", sys.exc_info()[0]
#            global_test_counter = 0
#            
#            #raw_input("go on with pressing a key")
#            
#        if line != None:
#            try:
#                index_after_ER.update_index_withLine(line)
#            except Exception:
#                print "Unexpected error:", sys.exc_info()[0]
#                print "error in index_after_ER.update_index_withLine(line) before return line"
#                print " \n\n"
#            
#        return line
#    
#    
