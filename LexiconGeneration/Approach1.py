import sys, re
from Util import CleanUp
import PatternUtil, PatternFinder
from Index import IndexUtils, Lookup
import LexiconGenerator, StandardLexiconEntries
from nltk.stem.wordnet import WordNetLemmatizer
import math
import Sparql



    
    
#
#def d_print(string):
#    if deBug == True:
#        print(string)
#        
#        
        



def createTermsForObjectProperty(PropertyEntities, anchor_index):
    """
    This function takes as input a list of subjects and objects from a given property.
    To maximise the number of sentences, which can be found in a corpora, not only the entities (subject, objects) are taken into account, but also all written combinations, which can be found in the Wikipediacorpus.
    These anchor-text were created before. It covers not only names, such as Barack Obama, but also typos such as Barak Obama etc.
    Works only for ObjectProperties
    
    Returns a list of the entieties, added with a inputs in all combinations from the anchor index.
    """
    
    term_hm = {}
    counter = 0
    x = None
    y = None 
    term = None 
    term_list = []
    
    """
    Use additional 
    """
    if len(PropertyEntities)/2 > 20000:
        result = []
        for item in range(0,len(PropertyEntities),2):
            x = PropertyEntities[item]
            y = PropertyEntities[item+1]
            x = x.encode("ascii","ignore")
            y = y.encode("ascii","ignore")
            if "(" in x:
                x = x.split("(")[0]
            if "(" in y:
                y = y.split("(")[0]
            result.append([x+" "+y,x,y])
        return result
    
    
    for item in range(0,len(PropertyEntities),2):
        
        x = None
        y = None 
        x = PropertyEntities[item]
        y = PropertyEntities[item+1]
#        just in case we have some strange codes in the input
        x = x.encode("ascii","ignore")
        y = y.encode("ascii","ignore")
        if y != None and x != None:
            """
            works in the moment only for the DBpedia ontology, as the anchor index is on the moment only mapped to DBpedia URIs but extracted from Wikipedia
            therefore it should provide for every ontology an improvement
            """
            x_uri = "http://dbpedia.org/resource/"+x.replace(" ","_")
            y_uri = "http://dbpedia.org/resource/"+y.replace(" ","_")
            if "(" in x:
                x = x.split("(")[0]
            if "(" in y:
                y = y.split("(")[0]
            x_list = [x]
            y_list = [y]
            
            tmp = anchor_index.searchForDbpediaURImax(x_uri,10)
            if len(tmp)!= 0:
                for entry in tmp:
                    x_list.append(entry[0])
            tmp = []
            tmp = anchor_index.searchForDbpediaURImax(y_uri,10)
            if len(tmp)!= 0:
                for entry in tmp:
                    y_list.append(entry[0])
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
#    print "len term_list: "+str(len(term_list))
    return term_list


def createDateList(y):
    """
    Takes a date in the format year - month - day.
    Format is always in numbers as it comes from dbpedia, e.g. 2001 - 01 - 1
    To get better results from Corpora such as Wikipedia, different kind of possible dates are created, always with the number of the month replaced bz the name of the month     
    
    Returns list of dates
    """
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
        y_list.append(y)
        
        return y_list
    except:
        return []

def createTermsForDataTypeProperty(uri, PropertyEntities, anchor_index):
    """
    This function is for Datatype properties only.
    Given are the entities (subject/object) from a property, where the object is only represented by numbers.
    To increase the number of sentences which are found in the corpus, for the subject alternative representation are tried to extract from the anchor index.
    The index containing all anchor text from Wikipedia, mapped to DBpedia URIs was created before.
    
    Returns a list with the entities from the input plus the alternative combinations of anchor entries and objects.    
    """
    sparql=Sparql.Connection()
    """
    The range of the URI to be determined, because for different ranges, different approaches are needed.
    """
    uri_range = sparql.askForRange(uri)
    """
    If no range could be found for the property, the function returns the original list, because without the information of the range,
    it can not be determined, which procedure is needed to increase the number of subject/object pairs.
    """
    if uri_range == None:
        result = []
        for item in range(0,len(PropertyEntities),2):
            x = PropertyEntities[item]
            y = PropertyEntities[item+1]
            x = x.encode("ascii","ignore")
            y = y.encode("ascii","ignore")
            if "(" in x:
                x = x.split("(")[0]
            if "(" in y:
                y = y.split("(")[0]
            result.append([x+" "+y,x,y])
        return result
#    print "the range of the URI is: "+str(uri_range)
    term_hm = {}
    x = None
    y = None 
    term_list = []
    for item in range(0,len(PropertyEntities),2):
        
        x = None
        y = None 
        x = PropertyEntities[item]
        y = PropertyEntities[item+1]
        x = x.encode("ascii","ignore")
        y = y.encode("ascii","ignore")
        if y != None and x != None:
            """
            As the anchor index is based on the DBpedia Ontology, the DBpedia URIs are used to finde similar entries in the index.
            """
            x_uri = "http://dbpedia.org/resource/"+x.replace(" ","_")
            if "(" in x:
                x = x.split("(")[0]

            x_list = [x]
            y_list = [y]
            
            tmp = anchor_index.searchForDbpediaURImax(x_uri,10)
            if len(tmp)!= 0:
                for entry in tmp:
                    x_list.append(entry[0])
            """
            Here now all possible combinations are created for the different ranges, for the different objects.
            """
            if "date" in uri_range:
                y_list.extend(createDateList(y))
            elif "gYear" in uri_range:
                y_list.extend(createDateList(y.split("T")[0]))
            else:
                x_list = []
                y_list = []
                
                
            
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

                                
                            term_list.append([term,xentry,yentry])
    return term_list



def normalisePattern(pattern):
    """
    Normalizes pattern to make it more intuitive to read.
    This is only for the user. The normalized patterns are saved to the path, were the lexicon is written.
    The system itself works still with the CONLL format.
    
    Returns the pattern in the new format
    """
    new_pattern = ""
    for x in pattern.split("  "):
        t = x.split(" ")
        new_pattern +=t[1]+" ("+t[7]+") _ "
    if new_pattern.endswith(" _ "):
        new_pattern = new_pattern[:-3]
                        
    return new_pattern

def createPatternFile(uri, path, name, hm):
    f = file(path + "PatternList" + name + ".txt", "w")
    write_string = ""
    overall_pattern_numer = 0
################## TODO: Save "normalized" set of patterns like for QA in extra function #######################
    different_pattern = 0
    hm_new = {}
    hm_test = {}
    for key, value in hm.iteritems():
    ###only for test#######
        
        if value > 1:
            overall_pattern_numer += value
            different_pattern += 1
            hm_new[key] = value
            
            new_pattern = normalisePattern(key)
            if hm_test.has_key(new_pattern):
                hm_test[new_pattern] = hm_test[new_pattern]+value
            else:
                hm_test[new_pattern] = value
            
    
    hm = {}
    hm = hm_new
    hm_new = {}
    alpha = 0.8
    
    ####only for test#####
    overall_pattern_numer = 0
    for key, value in hm_test.iteritems():
    ###only for test#######
        overall_pattern_numer += value
            
    
    for key, value in sorted(hm_test.iteritems(), key=lambda x:x[1], reverse=True):
        p = value / (overall_pattern_numer + 0.0)
        p_prime = (value - alpha) / (overall_pattern_numer + 0.0)
        p_3 = (overall_pattern_numer + 0.0)/value
        
        #write_string+="Pattern: "+key+"\t Occurrences: "+str(value)+"\t P(x|Property): "+str(p)+"\n"
        write_string += key + "\t" + str(value) + "\t" + uri + "\t" + str(math.log(p)) + "\t" + str(math.log(p_prime)) +"  "+ str(math.log(p_3)) +"\n"
    
    write_string = "Overall number: " + str(overall_pattern_numer) + " Different patterns: " + str(different_pattern) + "\n\n\n" + write_string
    f.write(write_string)
    f.close()
    return hm, overall_pattern_numer

def creatingLexiconEntry_for_singleURI(debug, uri, flag, path, index,live_index, anchor_index,en_de_lexicon, ontology_prefix = None ):   

    lmtzr = WordNetLemmatizer()
    global deBug 
    deBug = debug
    if ontology_prefix == None:
        name = (uri.replace("http://dbpedia.org/ontology/","")).replace("/","")
        name = (uri.replace("http://dbpedia.org/property/","")).replace("/","")
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


    if flag == True:
        term_list = []
        print "Gets entities for "+uri+" from the SPARQL endpoint"
        PropertyEntities = sparql.getPairsOfGivenProperties(uri)
#        PropertyEntities = ["Barack Obama","Michelle Obama"]
        print str(len(PropertyEntities)/2)+" number of entity pairs found"
        if sparql.askObjectProperty(uri) == True:
            print "Object property given"
            term_list = createTermsForObjectProperty(PropertyEntities,anchor_index)
            Lookup.lookupSortAndParse(term_list,index,live_index,flag,uri)
    
        else:
            #here add function for DataProperty
            print "Datatype property given"
            term_list = createTermsForDataTypeProperty(uri,PropertyEntities,anchor_index)
            Lookup.lookupSortAndParse(term_list,index,live_index,flag,uri)


    x_y_array = live_index.searchForXY(uri)
    print "Number of entity pairs returned from the index:"+str(len(x_y_array))
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
#                        print "Unexpected error in finding pattern:", sys.exc_info()[0]
                        #TODO: Fix exceptions.AttributeError'> in pattern generation!!!!!!!
                        pattern = None
                        

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
                    
                    
            except Exception:
                print "Unexpected error:", sys.exc_info()[0]
                print "error in creatingLexiconEntry_for_singleURI in lookup or some other function \n\n"

    

    pattern_once = 0
    
    hm , overall_pattern_numer = createPatternFile(uri, path, name, hm)
    
    
    lexico_array, tmp_pattern_once = PatternUtil.create_lexico_array(hm,uri,1,en_de_lexicon)
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
        tmp_entry = StandardLexiconEntries.createEntries(uri,en_de_lexicon)
        for x in tmp_entry:
            lemonEntriesHm[x]=""
#        label = sparql.getLabel(uri)
#        if "(" in label:
#            label = label.split("(")[0]
#        try:
#            entry = LexiconGenerator.NounPPFrame(label, uri, {})
#            lemonEntriesHm.append(entry)
#            entry = LexiconGenerator.NounPossisiveFrameWithoutMarker(label, uri)
#            lemonEntriesHm.append(entry)
#            entry = LexiconGenerator.AdjectivePPFrame(label, uri, {})
#            lemonEntriesHm.append(entry)
#        
#            #print "added"
#            
#            lemma = lmtzr.lemmatize(label,"v")
#            if lemma != label:
#                entry = LexiconGenerator.TransitiveFrame(lemma, uri, {})
#                lemonEntriesHm.append(entry)
#            else:
#                entry = LexiconGenerator.TransitiveFrame(label, uri, {})
#                lemonEntriesHm.append(entry)
#        except:
#            pass

        

    web_string = "<table><tr><td style=\"width: 50%;\"> "
    try:
        web_string += PatternUtil.create_html_table(lexico_array,hm_res_sentences,path,name,1)
    except:
        web_string += "No entry for the property "+uri+" could be created"
    web_string += "</td><td> "
    
    web_string += "</td></tr></table> "
    
    
    
    web_table0 = "<TABLE border=\"1\"><TR><TH>Property <TH>N. of overall Sentences<TH>N. of generated patterns<TH>N. of used patterns <TH><TR><TH><a href=\""+uri+"\">"+name+"</a><TD>"+str(total_number_sentence)+"<TD>"+str(overall_pattern_numer)+"<TD>"+str((len(hm)))+"<TD>"+"</a>"+"</TABLE>"
    
    web = web_table0+web_string
    
    #print "Number of used sentences: "+str(len(hm_res_sentences))
    
    hm.clear()
    
    return web, lemonEntriesHm
