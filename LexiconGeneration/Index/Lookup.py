import sys, os


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



def lookupSortAndParse(term_list,index,live_index, m_parser, flag,uri):
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
    config.read('settings.ini')
    procentOfDataset = config.getint("entries", "ProcentOfCorpus")

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
            result = []
            if x != y:
                result= index.search(term,1)
            
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
                        
                if found_x == True and found_y == True:
                    #Use each line only for one x-y pair
                    if line not in hm:
                        hm[line]=[x,y]
            
        except Exception:
            print "Unexpected error:", sys.exc_info()[0]
            #print ("Error in finding term: "+str(item))
     
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

    """
    parses always 10000 sentences at once.
    For other languages, here it has to be checked, which language is given and which parser has to be used.
    In the moment only English, but it will be changed to an interface, with different parsers.
    """    
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
                        
                    live_index.update_index_withLineArray(to_add)
                    parsed_sentences = []
                    to_add = []

            m_parser.parses_list_of_sentences(new_list, sfile)
            new_list = []
            parsed_sentences = load_file_return_list_of_sentences(sfile)
            to_add = []
            offset = p_counter%10000
            for i in range(0,len(parsed_sentences)):
                
                tmp = not_in_index[i+p_counter-offset]
                to_add.append([parsed_sentences[i],tmp[1],tmp[2],uri])

            live_index.update_index_withLineArray(to_add)
            parsed_sentences = []
            to_add = []

            parsed_sentences = []
            

        
        
        
        


