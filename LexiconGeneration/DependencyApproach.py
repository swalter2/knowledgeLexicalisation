import sys, re, ConfigParser
from Util import CleanUp
import PatternUtil, PatternFinder
from Index import IndexUtils, Lookup
import LexiconGenerator, StandardLexiconEntries
from nltk.stem.wordnet import WordNetLemmatizer
import math
import Sparql
language = None



    
    
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
    if len(PropertyEntities)/2 > 40000:
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
        month_array = []
        if language == "German":
            month_array = ["Januar", "Februar", "Maerz", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        elif language == "English":
            month_array = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        elif language == "Spanish":
            month_array = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        if month.startswith("0"):
            month = month[1:]
        month = month_array[int(month) - 1]
        while year.startswith("0"):
            year = year[1:0]
        
        y_list.append(year + " " + month + " " + day)
        y_list.append(day + " " + month + " " + year)
        y_list.append(day + ". " + month + " " + year)
        y_list.append(date[0]+"."+date[1]+"."+date[2])
        
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
    print ("uri_range",uri_range)
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
                
            elif "string" in uri_range:
                y_uri = "http://dbpedia.org/ontology/"+y.replace(" ","_")
                if "(" in y:
                    y = y.split("(")[0]
                tmp = anchor_index.searchForDbpediaURImax(y_uri,10)
                if len(tmp)!= 0:
                    for entry in tmp:
                        if entry[0] != "*":
                            y_list.append(entry[0])
                tmp = []
#             else:
#                 x_list = []
#                 y_list = []
                
            
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
    f = file(path + "PatternList" + name.replace("http://dbpedia.org/ontology","") + ".txt", "w")
    write_string = ""
#     overall_pattern_number = 0
#     for key, value in hm.iteritems():
#         overall_pattern_number += value
        
        
    different_pattern = 0
    hm_new = {}
    hm_test = {}
    for key, value in hm.iteritems():  
              
        ####SHOULD BE 1
        if value > 1:
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
    
    overall_pattern_number = 0
    for key, value in hm_test.iteritems():
        overall_pattern_number += value
    
            
    
    for key, value in sorted(hm_test.iteritems(), key=lambda x:x[1], reverse=True):
#         p = value / (overall_pattern_number + 0.0)
#         p_prime = (value - alpha) / (overall_pattern_number + 0.0)
#         p_3 = (overall_pattern_number + 0.0)/value
        
        #write_string+="Pattern: "+key+"\t Occurrences: "+str(value)+"\t P(x|Property): "+str(p)+"\n"
#         write_string += key + "\t" + str(value) + "\t" + uri + "\t" + str(math.log(p)) + "\t" + str(math.log(p_prime)) +"  "+ str(math.log(p_3)) +"\n"
        write_string += key + "\t" + str(value) + "\t" + uri +"\n"

    write_string = "Overall number: " + str(overall_pattern_number) + " Different patterns: " + str(different_pattern) + "\n\n\n" + write_string
    f.write(write_string)
    f.close()
    return hm, overall_pattern_number

def getEntities(path):
    f_in = open(path,"r")
    array = []
    for line in f_in:
        line = line.replace("\n","")
        tmp = line.split(" ## ")
        try:
            x = tmp[0]
            y = tmp[1]
            array.append(x)
            array.append(y)
        except:
            pass
    return array

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
    
    global language
    config = ConfigParser.ConfigParser()
    config.read('config.conf')    
    if config.get('system_language', 'language') == "English":
        language = "English"
    elif config.get('system_language', 'language') == "German":
        language = "German"
        
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
        PropertyEntities = []
        path_to_resource = config.get("index", "resource_folder")
        tmp_path = path_to_resource+"/"+uri.replace("http://dbpedia.org/ontology/","")
        print "Look in path "+tmp_path
        try:
            with open(tmp_path,"r"):
                print "Get entities for "+uri+" from resource folder"
                PropertyEntities = getEntities(tmp_path)

        except IOError:
            print "Get entities for "+uri+" from the SPARQL endpoint"
            PropertyEntities = sparql.getPairsOfGivenProperties(uri,tmp_path)
    
#         PropertyEntities = ["Barack Obama", "Michelle Obama"]
        print str(len(PropertyEntities)/2)+" number of entity pairs found"
        if sparql.askObjectProperty(uri) == True:
            print "Object property given"
            term_list = createTermsForObjectProperty(PropertyEntities,anchor_index)
            print ("number of terms",len(term_list))
            Lookup.lookupSortAndParse(term_list,index,live_index,flag,uri)
    
        else:
            #here add function for DataProperty
            print "Datatype property given"
            term_list = createTermsForDataTypeProperty(uri,PropertyEntities,anchor_index)
            print ("number of terms",len(term_list))
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
#                 s_t = ""
#                 for item in sentence:
#                     s_t += item.__return_as_string__()+"  "
#                 print (x,y,s_t)
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

    
    return_string = uri+";"+str(total_number_sentence)+";"+str(len(hm))+"\n"

    pattern_once = 0
    
    hm , overall_pattern_numer = createPatternFile(uri, path, name, hm)
    
    
    
    print "Created Pattern File"
    lexico_array, tmp_pattern_once, patterns_without_entry = PatternUtil.create_lexico_array(hm,uri,1,en_de_lexicon)
    pattern_once += tmp_pattern_once
    
    
    f_out = file(path + "NotUsedPattern" + name.replace("http://dbpedia.org/ontology","") + ".txt", "w")#
    write_string = ""
    for pattern_entry in patterns_without_entry:
        write_string += pattern_entry[0] + "\t" + str(pattern_entry[1]) + "\t" + uri +"\n"
    f_out.write(write_string)
    f_out.close()
    
    lemonEntriesHm = {}
    for item in lexico_array:
        lemonEntriesHm[item[0]]=""


#     web_string = "<table><tr><td style=\"width: 50%;\"> "
#     try:
#         web_string += PatternUtil.create_html_table(lexico_array,hm_res_sentences,path,name,1)
#     except:
#         web_string += "No entry for the property "+uri+" could be created"
#     web_string += "</td><td> "
#     
#     web_string += "</td></tr></table> "
#     
#     
#     
#     web_table0 = "<TABLE border=\"1\"><TR><TH>Property <TH>N. of overall Sentences<TH>N. of generated patterns<TH>N. of used patterns <TH><TR><TH><a href=\""+uri+"\">"+name+"</a><TD>"+str(total_number_sentence)+"<TD>"+str(overall_pattern_numer)+"<TD>"+str((len(hm)))+"<TD>"+"</a>"+"</TABLE>"
#     
#     web = web_table0+web_string
    web = ""
    
    #print "Number of used sentences: "+str(len(hm_res_sentences))
    print "created html side"
    print ("total_number_sentence used:",total_number_sentence)
    hm.clear()
    
    #return web, lemonEntriesHm ,return_string
    return web, lemonEntriesHm , total_number_sentence
