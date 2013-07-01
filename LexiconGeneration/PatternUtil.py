import LexiconGenerator, StandardLexiconEntries
import os, sys, ConfigParser
from Index import IndexUtils
from Util import  WordnetFunctions
import Sparql
from nltk.stem.wordnet import WordNetLemmatizer




#def d_print(string, debug):
#    if debug == True:
#        print(string)
#        



def create_html_table(lexico_array,hm_res_sentences,path,name,version):
    """
    Creates the html file, which makes it easier to look at the pattern and the corresponding sentences and lexicon entries
    """
    hilfsliste = {}
    lexico_array_new = []
    for item in lexico_array:
        name1 = str(item[0].split("\n")[0])
        name1 = name1.replace(" a lemon:LexicalEntry ;","")
        name1 = name1.replace(":","")
        
        if name1 in hilfsliste:
            pass
        else:
            hilfsliste[name1] = ""
            string0 = ""
            string1 = ""
            number = 0
            hilfsarray = []
            for i in lexico_array:
                try:
                    name_t = str(i[0].split("\n")[0])
                    name_t = name_t.replace(" a lemon:LexicalEntry ;","")
                    name_t = name_t.replace(":","")
                    
                    if str(name1) == str(name_t):
                        string0 += i[0]+"\n\n\n\n"
                        string1 += i[1]+"\n"
                        number += int(i[2])
                        hilfsarray.append(i[1])
                except:
                    pass
            tmp_array = []
            tmp_array.append(string0)
            tmp_array.append(string1)
            tmp_array.append(number)
            tmp_array.append(hilfsarray)
            lexico_array_new.append(tmp_array)
            
    web_string = ""
    counter = 0
    lexico_array = sort_array(lexico_array_new)
    web_string += "<TABLE border=\"1\"><TR><TH>#Pattern<TH>Entry"
    for item in lexico_array:
        counter += 1
        if counter < 26:
            f=file(path+"Result/"+str(version)+name+str(counter),"w")
            f.write(item[0])
            f.close()
            
            test = item[0].split("\n")[0]
            test = test.replace("a lemon:LexicalEntry ;","")
            test = test.replace(":","")
            
            f=file(path+"Result/"+str(version)+"P"+name+str(counter),"w")
            write_string = item[1]
            write_string += "\n##########################################################\n\n\n"
            
            for i in item[3]:
                #print i
                
                ##############################################################
                #I changed the pattern with a filter, and if so, the new patterns do not exist in the hm_res_sentences.
                #Therefore use try/catch to overgo the new pattern
                ##############################################################
                try:
                    write_string += hm_res_sentences[i]+"\n\n"
                except:
                    pass
                
            f.write(write_string)
            f.close()
            
            web_string+="<TR><TH><a href=\""+"Result/"+str(version)+"P"+name+str(counter)+"\">"+str(item[2])+"</a><TD><a href=\""+"Result/"+str(version)+name+str(counter)+"\">"+test+"</a>" #"\">Entry"+str(counter)+ 
    
            
    web_string += "</TABLE>"
    return web_string

def create_lexico_array(hm,uri,NumberOfPatterns, en_de_lexicon):
    lmtzr = WordNetLemmatizer()
    #Note: the NumberOfPatterns in the function call is later replaced by a procent value, depending on the number of patterns included into the system
    print "Number of patterns: "+str(len(hm))
    config = ConfigParser.ConfigParser()
    config.read('config.conf')
    procentOfPatterns = config.getfloat("entries", "PatternProcent")
    lexico_array = []
    sparql = Sparql.Connection()
    pattern_once = 0
    
    
    #check here how many hm are given in, and set NumberOfPatterns to at least 0.1% or other value
    NumberOfPatterns = int(len(hm)/100.0*procentOfPatterns)
    
    overall_pattern_numer = 0
    for key, value in hm.iteritems():
        overall_pattern_numer += value
    
    #take max the best ten
    
    best_counter = 0
    #only for test, set very high!
    max_counter = 10000
    #highest value first
    for key, value in sorted(hm.iteritems(), key=lambda x:x[1], reverse = True):
        best_counter += 1
            
        """
        Include different selecting strategies
        
        """
        ##########################
        ## Take all pattern with a certain percentage 
        ##########################
        if (((value/(overall_pattern_numer+0.0))*100) > procentOfPatterns and best_counter < max_counter+1) or overall_pattern_numer == len(hm):
        
        ##########################
        ## Take only the top 100 pattern
        ##########################
#        if best_counter < 101:   
        
        ##########################
        ## Take only the top 10 pattern
        ##########################
#        if best_counter < 11:
        
        ##########################
        ## Take every pattern which exists at least twice
        ## and ignore pattern which exists only once
        ##########################
#        if value > 1:


            try:
                entry_array=LexiconGenerator.createLexiconEntry(key, uri, False)
                for entry in entry_array:
                    tmp_array = []
                    tmp_array.append(entry)
                    tmp_array.append(key)
                    tmp_array.append(value)
                    lexico_array.append(tmp_array)
                if entry == None:
                    print "V1:Entry could not be created for pattern: "+key +"  "+str(value)
                    print
            except:
                print "V2:Entry could not be created for pattern: "+key +"  "+str(value)
                print

        else:
            pattern_once += 1
   
    tmp_entries = StandardLexiconEntries.createEntries(uri,en_de_lexicon)
    for x in tmp_entries:
        tmp_array = []
        tmp_array.append(x)
        tmp_array.append("Created by Guessing")
        tmp_array.append(1)
        lexico_array.append(tmp_array)


#    label = sparql.getLabel(uri)[0]
#    print "label: "+label
#    if "(" in label:
#        label = label.split("(")[0]
#    if label.endswith(" "):
#        label = label[:-1]
#        
#    """
#    Create some standard lexical entries, on base of the label of the property
#    """
#    entry = LexiconGenerator.NounPPFrame(label, uri, {})
#    tmp_array = []
#    tmp_array.append(entry)
#    tmp_array.append("Noun created by Guessing")
#    tmp_array.append(1)
#    lexico_array.append(tmp_array)
#    
#    entry = LexiconGenerator.AdjectivePPFrame(label, uri, {})
#    tmp_array = []
#    tmp_array.append(entry)
#    tmp_array.append("Adjective created by Guessing")
#    tmp_array.append(1)
#    lexico_array.append(tmp_array)
#    
#    entry = LexiconGenerator.NounPossisiveFrameWithoutMarker(label, uri)
#    #print entry
#    tmp_array = []
#    tmp_array.append(entry)
#    tmp_array.append("NounPossisive created by guessing")
#    tmp_array.append(1)
#    lexico_array.append(tmp_array)
#
#    
#    lemma = lmtzr.lemmatize(label,"v")
#
#    entry = LexiconGenerator.TransitiveFrame(lemma, uri, {})
#    tmp_array = []
#    tmp_array.append(entry)
#    tmp_array.append("Verb created by Wordnet")
#    tmp_array.append(1)
#    lexico_array.append(tmp_array)
#    
#    entry = LexiconGenerator.TransitiveFrame(label, uri, {})
#    tmp_array = []
#    tmp_array.append(entry)
#    tmp_array.append("Verb created by Wordnet")
#    tmp_array.append(1)
#    lexico_array.append(tmp_array)
    
        
    return lexico_array , pattern_once


    
    
def sort_array(array):
    'sort that the highest number comes first'
    return (sortby(array,2, True))


def sortby(somelist, n, bool):
    nlist = [(x[n], x) for x in somelist]
    nlist.sort(reverse=bool)
    return [val for (key, val) in nlist]

