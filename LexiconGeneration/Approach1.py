import sys, re
from Util import Sparql, CleanUp
import LgUtil, PatternFinder
from Index import IndexUtils, Lookup
import LexiconGenerator
from nltk.stem.wordnet import WordNetLemmatizer
import math



    
    

def d_print(string):
    if deBug == True:
        print(string)
        
        
        



def createTermsForObjectProperty(PropertyEntities, anchor_index):
    term_hm = {}
    counter = 0
    x = None
    y = None 
    term = None 
    term_list = []
    #print "retrieved "+str(len(PropertyEntities)/2)+" pairs"
    for item in range(0,len(PropertyEntities),2):
        
        x = None
        y = None 
        x = PropertyEntities[item]
        y = PropertyEntities[item+1]
        x = x.encode("ascii","ignore")
        y = y.encode("ascii","ignore")
        if y != None and x != None:
            x_uri = "http://dbpedia.org/resource/"+x.replace(" ","_")
            y_uri = "http://dbpedia.org/resource/"+y.replace(" ","_")
            if "(" in x:
                x = x.split("(")[0]
            if "(" in y:
                y = y.split("(")[0]
            x_list = [x]
            y_list = [y]
            
            tmp = anchor_index.searchForDbpediaURI(x_uri)
            if len(tmp)!= 0:
                for entry in tmp:
                    x_list.append(entry[0])
            #print "added "+str(len(tmp))+" to list"
            tmp = []
            tmp = anchor_index.searchForDbpediaURI(y_uri)
            if len(tmp)!= 0:
                for entry in tmp:
                    y_list.append(entry[0])
            #print "added "+str(len(tmp))+" to list"       
            for xentry in x_list:
                for yentry in y_list:
                    if xentry != yentry:
                        term = xentry +" "+ yentry
                        if term_hm.has_key(term):
                            pass
                        else:
                            term_hm[term] = ""
                            array = re.findall(r'[\w\s]+',xentry)
                            xentry = ""
                            for a in array:
                                xentry+=a
                            array = re.findall(r'[\w\s]+',yentry)
                            yentry = ""
                            for a in array:
                                yentry+=a
                            if xentry.startswith(" "):
                                xentry=xentry[1:]
                            if yentry.startswith(" "):
                                yentry=yentry[1:]
                                
                            if xentry == "" or yentry == "" or xentry == None or yentry == None or xentry in yentry or yentry in xentry:
                                pass
                            else:
                                term_list.append([term,xentry,yentry])
    print "len term_list: "+str(len(term_list))
    #raw_input("wait")
    return term_list


def createDateList(y):
    y_list = []
    try:
    
        date = y.split("-")
        year = date[0]
        month = date[1]
        day = date[2]
        month_array = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        if month.startswith("0"):
            month = month[1:]
        month = month_array[int(month) - 1]
        while year.startswith("0"):
            year = year[1:0]
        
        y_list.append(year + " " + month + " " + day)
        y_list.append(day + " " + month + " " + year)
        y_list.append(day + ". " + month + " " + year)
        
        return y_list
    except:
        return []

def createTermsForDataTypeProperty(uri, PropertyEntities, anchor_index):
    sparql=Sparql.Connection()
    uri_range = sparql.askForRange(uri)
    print "uri_range"+str(uri_range)
    term_hm = {}
    x = None
    y = None 
    term_list = []
    #print "retrieved "+str(len(PropertyEntities)/2)+" pairs"
    for item in range(0,len(PropertyEntities),2):
        
        x = None
        y = None 
        x = str(PropertyEntities[item])
        y = str(PropertyEntities[item+1])
        if y != None and x != None:
            x_uri = "http://dbpedia.org/resource/"+x.replace(" ","_")
            if "(" in x:
                x = x.split("(")[0]

            x_list = [x]
            y_list = [y]
            
            tmp = anchor_index.searchForDbpediaURI(x_uri)
            if len(tmp)!= 0:
                for entry in tmp:
                    x_list.append(entry[0])
            #print "added "+str(len(tmp))+" to list"
            #print uri
            
            if "date" in uri_range:
                y_list.extend(createDateList(y))
            elif "gYear" in uri_range:
                y_list.extend(createDateList(y.split("T")[0]))
            else:
                x_list = []
                y_list = []
                
                
            
            #print "added "+str(len(tmp))+" to list"       
            for xentry in x_list:
                for yentry in y_list:
                    if xentry != yentry:
                        term = xentry +" "+ yentry
                        if term_hm.has_key(term):
                            pass
                        else:
                            term_hm[term] = ""
                            array = re.findall(r'[\w\s]+',xentry)
                            xentry = ""
                            for a in array:
                                xentry+=a
                                #anyway there are only number
#                            array = re.findall(r'[\w\s]+',yentry)
#                            yentry = ""
#                            for a in array:
#                                yentry+=a
                                
                            term_list.append([term,xentry,yentry])
    print "len term_list: "+str(len(term_list))
    #raw_input("wait")
    return term_list


#def createTermsForObjectProperty(PropertyEntities, anchor_index):
#    term_hm = {}
#    counter = 0
#    x = None
#    y = None 
#    term = None 
#    term_list = []
#    for line in PropertyEntities:
#        counter += 1
#        line = line[1:] if line[:1] == " " else line
#        if counter == 1:
#            x = str(line)
#        if counter == 2:
#            y = str(line)
#            counter = 0
#            if x != None and y != None:
#                process_any_further = True
#                #check here, if pattern already exists in term_hm
#                if term_hm.has_key(x + y) or term_hm.has_key(y + x):
#                    process_any_further = False
#                else:
#                    term_hm[x + y] = ""
#                    term_hm[y + x] = ""
#                if "(" in x:
#                    tmp = x.split("(")
#                    x = x if len(tmp) == 0 else tmp[0]
#                if "(" in y:
#                    tmp = y.split("(")
#                    y = y if len(tmp) == 0 else tmp[0]
#                if x.endswith(" "):
#                    x = x[:-1]
#                if y.endswith(" "):
#                    y = y[:-1]
#                #if x and y are equal, dont use them
#                if x == y:
#                    process_any_further = False
#                if process_any_further == True:
#            #first set Term, because otherwise results will be changed and less good
#                    term = x + " " + y.replace("-", " ")
#                    x, y = CleanUp.clean_x_y(x.replace("-", " "), y.replace("-", " "))
#                else:
#                    term = None
#            term = None if (x == None or y == None) else term
#            if term != None:
#                term_list.append([term, x, y])
#    
#    PropertyEntities = []
#    return term_list


def creatingLexiconEntry_for_singleURI(debug, uri, flag, path, index,live_index,m_parser, anchor_index, ontology_prefix = None ):   

    lmtzr = WordNetLemmatizer()
    global deBug 
    deBug = debug
    if ontology_prefix == None:
        name = (uri.replace("http://dbpedia.org/ontology/","")).replace("/","")
    else:
        name = (uri.replace(ontology_prefix,"")).replace("/","")
    sparql=Sparql.Connection()

    hm={}
    hm_res_sentences = {}
    hm_used = {}
    total_number_sentence=0
    used_sentence=0
    sentence_for_rules=0
    
    number_of_error_sentences = 0
    number_of_error_res = 0
    error_res_sentences = ""
    error_sentences = ""


    
#    term_list=[["Barack Obama Michelle Obama","Barack Obama","Michelle Obama"]]
#    term_list.append(["Margaret Sullavan William Wyler","Margaret Sullavan","William Wyler"])
#    term_list.append(["Napoleon Marie Louise, Duchess of Parma","Napoleon","Marie Louise, Duchess of Parma"])


#    new_sentence_array = Lookup.lookupSortAndParse(term_list,index,live_index,m_parser,flag)

    if flag == True:
        term_list = []
        PropertyEntities = sparql.getPairsOfGivenProperties(uri)
        print str(len(PropertyEntities)/2)+" number of pairs"
        if sparql.askObjectProperty(uri) == True:
            print "in Object Case"
            term_list = createTermsForObjectProperty(PropertyEntities,anchor_index)
            Lookup.lookupSortAndParse(term_list,index,live_index,m_parser,flag,uri)
    
        else:
            #here add function for DataProperty
            print "in Property Case"
            term_list = createTermsForDataTypeProperty(uri,PropertyEntities,anchor_index)
            Lookup.lookupSortAndParse(term_list,index,live_index,m_parser,flag,uri)
            
    #lookupSortAndParse nur wenn prasen flag auf True ist,
    #ansonsten hier direkt nach x/y suchen im index der geparsten saetze
#    print len(new_sentence_array)
#    for item in new_sentence_array:
    #for entry1 in [1]:
    x_y_array = live_index.searchForXY(uri)
    print "Number of x y pairs:"+str(len(x_y_array))
    for entry1 in x_y_array:
        x = entry1[0]
        y = entry1[1]

        for parsed_sentence in live_index.searchXYPair(x,y):
            #only uses x/y/sentence combination once!
            try:
                sentence = parsed_sentence
                total_number_sentence+=1
                used_sentence+=1       
                try:
                    
                    try:
                        pattern = PatternFinder.find_pattern_between_x_and_y(x,y,sentence)
                    except:
                        pattern = None
                        
                    if pattern == None:
                        number_of_error_res += 1
                        if number_of_error_res <1500:
                            error_res_sentences += " x="+x+" y="+y+" "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n"
                            
                    if pattern != None:
                        if pattern in hm_res_sentences:
                            string = hm_res_sentences[pattern]
                            string += "x="+x+" y="+y+"   "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n\n"
                            hm_res_sentences[pattern] = string
                        else:
                            string = "x="+x+" y="+y+"   "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n\n"
                            hm_res_sentences[pattern] = string
                except:
                    pattern = None
                    
                if pattern != None:
                    sentence_for_rules+=1  
                    if pattern in hm:
                        hm[pattern]=int(hm[pattern])+1
                        hm_used[pattern]=sentence
                    else:
                        hm[pattern]=1
                else:
                    pass
                    
                #raw_input()
                    
            except Exception:
                print "Unexpected error:", sys.exc_info()[0]
                print "error in creatingLexiconEntry_for_singleURI in lookup or some other function \n\n"

    

    pattern_once = 0
    
    f=file(path+"PatternList"+name+".txt","w")
    write_string = ""
    overall_pattern_numer = 0
    
#    #change hm, so that highest value is first!!!
    #hm= sorted(hm.iteritems(), key=lambda x:x[1], reverse = True)
    
#    for key, value in sorted(hm.iteritems(), key=lambda x:x[1], reverse = True):
#        overall_pattern_numer += value
        
    different_pattern = 0
    hm_new = {}
    for key, value in hm.iteritems():
        ###only for test#######
        if value >1:
            overall_pattern_numer += value
            different_pattern += 1
            hm_new[key]=value
    hm = {}
    hm = hm_new
    hm_new = {}
    alpha = 0.5
    #for key, value in hm.iteritems():
    #overall_p = 0
    for key, value in sorted(hm.iteritems(), key=lambda x:x[1], reverse = True): 
        p = value/(overall_pattern_numer+0.0)
        p_prime = (value-alpha)/(overall_pattern_numer+0.0)
        #write_string+="Pattern: "+key+"\t Occurrences: "+str(value)+"\t P(x|Property): "+str(p)+"\n"

        write_string+=key+"\t"+str(value)+"\t"+uri+"\t"+str(math.log(p))+"\t"+str(math.log(p_prime))+"\n"
        #overall_p += p
    #raw_input(str(overall_p))
        
    write_string = "Overall number: "+str(overall_pattern_numer)+" Different patterns: "+str(different_pattern)+"\n\n\n"+write_string
        
    f.write(write_string)
    
    f.close()
    
    
    lexico_array, tmp_pattern_once = LgUtil.create_lexico_array(hm,uri,1)
    pattern_once += tmp_pattern_once
    
    
    lemonEntriesHm = {}
    for item in lexico_array:
        lemonEntriesHm[item[0]]=""
        
    ##################################
    ##################################
    #
    #Problem: Sometimes NO Sentence is found, or used => No Pattern => No entry
    #=> guess entry for Noun and if possible verb
    #
    ##################################
    ##################################
    if total_number_sentence == 0 or len(lemonEntriesHm) == 0:
        label = sparql.getLabel(uri)
        if "(" in label:
            label = label.split("(")[0]
        try:
            entry = LexiconGenerator.NounPPFrame(label, uri, {})
            lemonEntriesHm.append(entry)
            entry = LexiconGenerator.NounPossisiveFrameWithoutMarker(label, uri)
            lemonEntriesHm.append(entry)
            entry = LexiconGenerator.AdjectivePPFrame(label, uri, {})
            lemonEntriesHm.append(entry)
        
            #print "added"
            
            lemma = lmtzr.lemmatize(label,"v")
            if lemma != label:
                entry = LexiconGenerator.TransitiveFrame(lemma, uri, {})
                lemonEntriesHm.append(entry)
            else:
                entry = LexiconGenerator.TransitiveFrame(label, uri, {})
                lemonEntriesHm.append(entry)
        except:
            pass

        

    web_string = "<table><tr><td style=\"width: 50%;\"> "
    try:
        web_string += LgUtil.create_html_table(lexico_array,hm_res_sentences,path,name,1)
    except:
        web_string += "No entry for the property "+uri+" could be created"
    web_string += "</td><td> "
    
    web_string += "</td></tr></table> "
    
    
    
    f=file(path+"Error"+name,"w")
    error_sentences = error_sentences.encode("ascii","ignore")
    f.write(error_sentences)
    f.close()
    f=file(path+"PError"+name,"w")
    error_res_sentences = error_res_sentences.encode("ascii","ignore")
    f.write(error_res_sentences)
    f.close()
    
    web_table0 = "<TABLE border=\"1\"><TR><TH>Property <TH>N. of overall Sentences<TH>N. of generated patterns<TH>N. of \" Problem\" Sentences<TH> N. of used patterns <TH> N. of sentences without pattern <TH><TR><TH><a href=\""+uri+"\">"+name+"</a><TD>"+str(total_number_sentence)+"<TD>"+str(overall_pattern_numer)+"<TD>"+"<a href=\""+"Error"+name+"\">"+str(number_of_error_sentences)+"</a>"+"<TD>"+str((len(hm)))+"<TD>"+"<a href=\""+"PError"+name+"\">"+str(number_of_error_res)+"</a>"+"</TABLE>"
    
    web = web_table0+web_string
    
    print "Number of used sentences: "+str(len(hm_res_sentences))
    
    hm.clear()
    
    return web, lemonEntriesHm






#def given_x_y_uri(debug, uri,x_y_array, flag, path, index, m_parser, live_index, NumberOfPatterns):
#    
#    #_init_()
#   
#   
#    global deBug 
#    deBug = debug
#    
#    #print "URI: "+uri
#    name = (uri.replace("http://dbpedia.org/ontology/","")).replace("/","")
#    #print "Name: "+name
#    
#    result = []
#    
#    hm={}
#    get1 = hm.get
#    hm2={}
#    get2 = hm.get
#    
#    hm_res_sentences = {}
#    hm_res_sentences2 = {}
#    
#    term_hm = {}
#    
#    hm_used = {}
#    hm_used2 = {}
#    counter=0
#    x = None
#    y = None
#    term = None
#    total_number_sentence=0
#    used_sentence=0
#    sentence_for_rules=0
#    version1_number = 0
#    version2_number = 0
#    
#    number_of_error_sentences = 0
#    number_of_error_res = 0
#    error_res_sentences = ""
#    error_sentences = ""
#    blub_gram = 0
#    term_list = []
#    for item in x_y_array:
#        term = item[0]+" "+item[1]
#        #print "Generated term: "+term
#        term_list.append(term)
#    Lookup.lookup_and_parse_new(term_list, flag, index, m_parser,live_index)
#    
#    x = None
#    y= None
#    term = None
#    for item in x_y_array:
#        x = item[0]
#        y = item[1]
#        
#        #first set Term, because otherwise results will be changed and less good
#        term=(x+" "+y).replace("-"," ")
#        x, y = CleanUp.clean_x_y(x.replace("-"," "),y.replace("-"," "))
#
#        Tterm_tmp=y+" "+x
#        Tterm_tmp=Tterm_tmp.replace("-"," ")
#        if x.lower()== y.lower() or x.lower() in y.lower() or y.lower() in x.lower():
#            term = None
#        if term in term_hm or Tterm_tmp in term_hm:
#            term = None
#        else:
#            term_hm[term]=""
#
#        if term!=None and term!=" ":
#            try:
#
#                result1 = Lookup.lookup(term, False, index, m_parser, live_index)
#                
#                d_print(str(len(result1))+ " number of sentences found for term "+term)
#                
#                
#                #raw_input()
#                for parsed_sentence in result1:
#                    version1 = True
#                    go_on = True
#                    sentence = None
#                    fail = False
#                    if x == "" or y == "" or x.lower()==y.lower():
#                        go_on = False
#                    else:
#                        sentence, go_on = LgUtil.replace_parsedSentence_with_x_y(parsed_sentence,x,y)
#                        total_number_sentence+=1
#                        used_sentence+=1
#                        
#                        if go_on == False:
#                            fail = True
#                    try:
#                        if go_on == True:
#                            try:
#                                pattern , version1 = PatternFinder.find_pattern_between_x_and_y(x,y,sentence)
#                            except:
#                                pattern = None
#                                
#                            if pattern == None:
#                                number_of_error_res += 1
#                                if number_of_error_res <1500:
#                                    error_res_sentences += " x="+x+" y="+y+" "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n"
#                                    
#                            if pattern != None:
#                                
#                                if version1 == True:
#                                    if pattern in hm_res_sentences:
#                                        string = hm_res_sentences[pattern]
#                                        string += "x="+x+" y="+y+"   "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n\n"
#                                        hm_res_sentences[pattern] = string
#                                    else:
#                                        
#                                        version1_number +=1
#                                          
#                                        #print IndexUtils.reverse_sentence_wrapper(sentence)
#                                        string = "x="+x+" y="+y+"   "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n\n"
#                                        hm_res_sentences[pattern] = string
#                                else:
#                                    if pattern in hm_res_sentences2:
#                                        string = hm_res_sentences2[pattern]
#                                        string += "x="+x+" y="+y+"   "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n\n"
#                                        hm_res_sentences2[pattern] = string
#                                    else:
#                                        
#                                        version2_number +=1
#                                          
#                                        #print IndexUtils.reverse_sentence_wrapper(sentence)
#                                        string = "x="+x+" y="+y+"   "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n\n"
#                                        hm_res_sentences2[pattern] = string
#                            
#                        else:
#                            if fail == True:
#                                number_of_error_sentences +=1
#                                #only add the first 1000 error sentences to save disk space
#                                if number_of_error_sentences <1500:
#                                    error_sentences += " x="+x+" y="+y+" "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n"
#                            pattern = None
#                    except:
#                        pattern = None
#                    #print pattern
#                        
#                    if pattern != None:
#                        sentence_for_rules+=1
#                        if pattern[(len(pattern)-2):] == "  ":
#                            pattern=pattern[:(len(pattern)-2)]
#                        
#                        #here I have to split into version1 and version2
#                        if version1 == True:
#                            hm[pattern] = get1(pattern, 0) + 1
#                            hm_used[pattern]=sentence
#                        else:
#                            hm2[pattern] = get2(pattern, 0) + 1
#                            hm_used2[pattern]=sentence
#                                
#                    else:
#                        pass
#                        
#                    #raw_input()
#                    
#            except Exception:
#                print "Unexpected error:", sys.exc_info()[0]
#                print "error in creatingLexiconEntry_for_singleURI in lookup or some other function \n\n"
#    
#
#
#    #f=file(path+name,"w")
#    print str(total_number_sentence)+"\n\n"
#    
#    lexico_array = []
#    lexico_array2 = []
#    pattern_once = 0
#
#    lexico_array, tmp_pattern_once = LgUtil.create_lexico_array(hm,uri,NumberOfPatterns)
#    pattern_once += tmp_pattern_once
#    
#    lexico_array2, tmp_pattern_once = LgUtil.create_lexico_array(hm2,uri,NumberOfPatterns)
#    pattern_once += tmp_pattern_once
#    
#    
#    web_string = "<table><tr><td style=\"width: 50%;\"> "
#    #web_string += LgUtil.create_html_table(lexico_array,hm_res_sentences,path,name,1)
#    web_string += "</td><td> "
#    
#    #web_string += LgUtil.create_html_table(lexico_array2,hm_res_sentences2,path,name,2)
#    web_string += "</td></tr></table> "
#    
#    
#    
#    f=file(path+"Error"+name,"w")
#    f.write(error_sentences)
#    f.close()
#    f=file(path+"PError"+name,"w")
#    f.write(error_res_sentences)
#    f.close()
#    
#    web_table0 = "<TABLE border=\"1\"><TR><TH>Property <TH>N. of overall Sentences<TH>N. of generated patterns<TH>N. of \" Problem\" Sentences<TH> N. of used patterns <TH> N. of sentences without pattern <TH><TR><TH><a href=\""+uri+"\">"+name+"</a><TD>"+str(total_number_sentence)+"<TD>"+str(len(hm)+len(hm2))+"<TD>"+"<a href=\""+"Error"+name+"\">"+str(number_of_error_sentences)+"</a>"+"<TD>"+str((len(hm)+len(hm2))-pattern_once)+"<TD>"+"<a href=\""+"PError"+name+"\">"+str(number_of_error_res)+"</a>"+"</TABLE>"
#    
#    web = web_table0+web_string +"version1: "+str(version1_number)+" and version2: "+str(version2_number)+"    "
#    
#    
#    #print "bla: "+str(len(hm_res_sentences))
#    return web
#
#
#
#def given_x_y_uriGivenSentences(debug, uri,x_y_array,sentence_array, flag, path, NumberOfPatterns):
#    
#    #_init_()
#   
#   
#    global deBug 
#    deBug = debug
#    
#    print "URI: "+uri
#    name = (uri.replace("http://dbpedia.org/ontology/","")).replace("/","")
#    #print "Name: "+name
#    
#    #raw_input("name presented")
#    
#    result = []
#    
#    hm={}
#    get1 = hm.get
#    hm2={}
#    get2 = hm.get
#    
#    hm_res_sentences = {}
#    hm_res_sentences2 = {}
#    
#    term_hm = {}
#    
#    hm_used = {}
#    hm_used2 = {}
#    total_number_sentence=0
#    used_sentence=0
#    sentence_for_rules=0
#    version1_number = 0
#    version2_number = 0
#    
#    number_of_error_sentences = 0
#    number_of_error_res = 0
#    error_res_sentences = ""
#    error_sentences = ""
#    
#    x = None
#    y= None
#    term = None
#    for item in x_y_array:
#        x = item[0]
#        y = item[1]
#        
#        #first set Term, because otherwise results will be changed and less good
#        term=(x+" "+y).replace("-"," ")
#        x, y = CleanUp.clean_x_y(x.replace("-"," "),y.replace("-"," "))
#
#        Tterm_tmp=y+" "+x
#        Tterm_tmp=Tterm_tmp.replace("-"," ")
#        if x.lower()== y.lower() or x.lower() in y.lower() or y.lower() in x.lower():
#            term = None
#        if term in term_hm or Tterm_tmp in term_hm:
#            term = None
#        else:
#            term_hm[term]=""
#
#        if term!=None and term!=" ":
#            try:
#                result1 = returning_sentences_containing_term(sentence_array, term)
#                #result1 = Lookup.lookup(term, False, index, m_parser, live_index)
#                
#                d_print(str(len(result1))+ " number of sentences found for term "+term)
#                #print(str(len(result1))+ " number of sentences found for term "+term)
#                #print "x: "+x
#                #print "y: "+y
#                #raw_input("see above")
#                #for r in result1:
#                #    print r.__str__()
#                #raw_input("number of s")
#                
#                #raw_input()
#                for parsed_sentence in result1:
#                    #print "parsed_sentence before: "+parsed_sentence.__str__()
#                    #raw_input("before")
#                    version1 = True
#                    go_on = True
#                    #sentence = None
#                    sentence = parsed_sentence
#                    fail = False
#                    if x == "" or y == "" or x.lower()==y.lower():
#                        go_on = False
#                    else:
#                        go_on = True
#                        #try:
#                        #    sentence, go_on = LgUtil.replace_parsedSentence_with_x_y(parsed_sentence,x,y)
#                        #    
#                        #except:
#                        #    raw_input("Error in replace x and y")
#                        #print "x: "+x
#                        #print "y: "+y
#                        #print "sentence: "+sentence.__str__()
#                        #print "parsed_sentence "+parsed_sentence.__str__()
#                        #raw_input("See output")
#                        total_number_sentence+=1
#                        used_sentence+=1
#                        
#                        if go_on == False:
#                            fail = True
#                    try:
#                        if go_on == True:
#                            try:
#                                pattern , version1 = PatternFinder.find_pattern_between_x_and_y(x,y,sentence)
#                            except:
#                                pattern = None
#                                
#                            if pattern == None:
#                                number_of_error_res += 1
#                                if number_of_error_res <1500:
#                                    error_res_sentences += " x="+x+" y="+y+" "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n"
#                                    
#                            if pattern != None:
#                                
#                                if version1 == True:
#                                    if pattern in hm_res_sentences:
#                                        string = hm_res_sentences[pattern]
#                                        string += "x="+x+" y="+y+"   "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n\n"
#                                        hm_res_sentences[pattern] = string
#                                    else:
#                                        
#                                        version1_number +=1
#                                          
#                                        #print IndexUtils.reverse_sentence_wrapper(sentence)
#                                        string = "x="+x+" y="+y+"   "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n\n"
#                                        hm_res_sentences[pattern] = string
#                                else:
#                                    if pattern in hm_res_sentences2:
#                                        string = hm_res_sentences2[pattern]
#                                        string += "x="+x+" y="+y+"   "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n\n"
#                                        hm_res_sentences2[pattern] = string
#                                    else:
#                                        
#                                        version2_number +=1
#                                          
#                                        #print IndexUtils.reverse_sentence_wrapper(sentence)
#                                        string = "x="+x+" y="+y+"   "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n\n"
#                                        hm_res_sentences2[pattern] = string
#                            
#                        else:
#                            if fail == True:
#                                number_of_error_sentences +=1
#                                #only add the first 1000 error sentences to save disk space
#                                if number_of_error_sentences <1500:
#                                    error_sentences += " x="+x+" y="+y+" "+IndexUtils.reverse_sentence_wrapper(sentence)+"\n"
#                            pattern = None
#                    except:
#                        pattern = None
#                    #print pattern
#                        
#                    if pattern != None:
#                        sentence_for_rules+=1
#                        if pattern[(len(pattern)-2):] == "  ":
#                            pattern=pattern[:(len(pattern)-2)]
#                        
#                        #here I have to split into version1 and version2
#                        if version1 == True:
#                            hm[pattern] = get1(pattern, 0) + 1
#                            hm_used[pattern]=sentence
#                            #if pattern in hm:
#                            #    hm[pattern]=int(hm[pattern])+1
#                            #    hm_used[pattern]=sentence
#                            #else:
#                            #    hm[pattern]=1
#                        else:
#                            hm2[pattern] = get2(pattern, 0) + 1
#                            hm_used2[pattern]=sentence
#                            #if pattern in hm2:
#                            #    hm2[pattern]=int(hm2[pattern])+1
#                            #    hm_used2[pattern]=sentence
#                            #else:
#                            #    hm2[pattern]=1
#                                
#                    else:
#                        pass
#                        
#                    #raw_input()
#                    
#            except Exception:
#                print "Unexpected error:", sys.exc_info()[0]
#                print "error in creatingLexiconEntry_for_singleURI in lookup or some other function \n\n"
#    
#
#
#    #f=file(path+name,"w")
#    print str(total_number_sentence)+"\n\n"
#    
#    lexico_array = []
#    lexico_array2 = []
#    pattern_once = 0
#
#    lexico_array, tmp_pattern_once = LgUtil.create_lexico_array(hm,uri,NumberOfPatterns)
#    pattern_once += tmp_pattern_once
#    
#    lexico_array2, tmp_pattern_once = LgUtil.create_lexico_array(hm2,uri,NumberOfPatterns)
#    pattern_once += tmp_pattern_once
#    
#    
#    web_string = "<table><tr><td style=\"width: 50%;\"> "
#    #web_string += LgUtil.create_html_table(lexico_array,hm_res_sentences,path,name,1)
#    web_string += "</td><td> "
#    
#    #web_string += LgUtil.create_html_table(lexico_array2,hm_res_sentences2,path,name,2)
#    web_string += "</td></tr></table> "
#    
#    
#    
#    f=file(path+"Error"+name,"w")
#    f.write(error_sentences)
#    f.close()
#    f=file(path+"PError"+name,"w")
#    f.write(error_res_sentences)
#    f.close()
#    
#    web_table0 = "<TABLE border=\"1\"><TR><TH>Property <TH>N. of overall Sentences<TH>N. of generated patterns<TH>N. of \" Problem\" Sentences<TH> N. of used patterns <TH> N. of sentences without pattern <TH><TR><TH><a href=\""+uri+"\">"+name+"</a><TD>"+str(total_number_sentence)+"<TD>"+str(len(hm)+len(hm2))+"<TD>"+"<a href=\""+"Error"+name+"\">"+str(number_of_error_sentences)+"</a>"+"<TD>"+str((len(hm)+len(hm2))-pattern_once)+"<TD>"+"<a href=\""+"PError"+name+"\">"+str(number_of_error_res)+"</a>"+"</TABLE>"
#    
#    web = web_table0+web_string +"version1: "+str(version1_number)+" and version2: "+str(version2_number)+"    "
#    
#    
#    #print "bla: "+str(len(hm_res_sentences))
#    return web
#
#
##all_johns = [p for p in PhoneDirectory if 'Joh' in p]
#
#
#def returning_sentences_containing_term(sentence_array, term):
#    term_array = term.split(" ")
#    
#    #print "len(sentence_array):"+str(len(sentence_array))
#    #print "term: "+term
#    
#    #raw_input("wait")
#    
#    lower = str.lower
#    #result1 = []
#    hm = {}
#    number = 0
#    #return [sentence for sentence in sentence_array if (t in sentence for t in term.split(" "))]
#    result = []
#    for sentence in sentence_array:
#        sentence=sentence.replace("\t"," ")
#        sentence=sentence.replace("\n"," ")
#        
#        if sentence[len(sentence)-2:]=="  ":
#            sentence = sentence[:len(sentence)-2]
#        #print "sentence: "+sentence
#        #print str(lower(sentence).split("\t"))
#        overall_bool = True
#        for item in term_array:
#            #print term_array
#            b = (True if lower(item) in lower(sentence) else False)
#            #print "lower(sentence):" +lower(sentence)
#            if b == True:
#                hm[sentence]=""
#            if b==False:
#                overall_bool = False
#        if overall_bool:
#            number += 1
#            #print sentence
#            #raw_input("wait1")
#            #try:
#                #print sentence
#            #result1.append(sentence)
#            result.append(IndexUtils.sentence_wrapper(sentence)) 
#                
#                #raw_input("sentence appended")
#            #except:
#            #    pass
#    #if number >0:
#    #    print "num of s "+str(len(result))
#    #    print "num of s1 "+str(len(result))
#    #    print "number: "+str(number)
#        #raw_input("in returning s")
#    #result = []
#    #for key in hm:
#    #    result.append(IndexUtils.sentence_wrapper(key)) 
#        
#    #print (str(len(result)))
#    
#    #for item in result:
#    #    print "line: "+item.__str__()
#        
#    #print "Done"
#    
#    return result       
#        
