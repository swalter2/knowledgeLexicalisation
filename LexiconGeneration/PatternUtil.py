import LexiconGenerator, StandardLexiconEntries
import os, sys, ConfigParser
from Index import IndexUtils
from Util import  WordnetFunctions
import Sparql




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
    print "Number of patterns: "+str(len(hm))
    config = ConfigParser.ConfigParser()
    config.read('config.conf')
    procentOfPatterns = config.getfloat("entries", "PatternProcent")
    topkentries = procentOfPatterns
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
    lem_entries_hm = {}
    f_hm = {}
    try:
        f = open("/home/swalter/wrongpattern","r")
        for line in f:
            f_hm[line.replace("\n","")] = ""
        f.close()
    except:
        pass
            
    blub_array = []
    for key, value_pattern in sorted(hm.iteritems(), key=lambda x:x[1], reverse = True):
        best_counter += 1
        """
        Different selecting strategies based on the lemon entries
        
        """
        try:
            entry_array=LexiconGenerator.createLexiconEntry(key, uri, False)
            for entry in entry_array:
                blub_array.append((key,entry))
                if lem_entries_hm.has_key(entry):
                    value = lem_entries_hm[entry]
#                     value += 1
                    value += value_pattern
                    lem_entries_hm[entry] = value
                else:
                    lem_entries_hm[entry] = value_pattern
#                     lem_entries_hm[entry] = 1

        except:
            f_hm[key]=""
            print "V3:Entry could not be created for pattern: "+key +"  "+str(value)
            print
            print
#     f = open("/home/swalter/wrongpattern","w")
#     for key in f_hm:
#         f.write(key+"\n")
#     f.close()
#     f = open("/home/swalter/rightpattern","w")
#     for blub in blub_array:
#         f.write(str(blub)+"\n")
#     f.close()
            
#     for entry in lem_entries_hm:
#         if value > 2:
#             tmp_array = []
#             tmp_array.append(entry)
#             tmp_array.append("")
#             tmp_array.append(value)
#             lexico_array.append(tmp_array)
#         else:
#             pattern_once += 1

    lem_counter = 0
    for key, value in sorted(lem_entries_hm.iteritems(), key=lambda x:x[1], reverse = True):
#         print key
        lem_counter += 1
        if lem_counter < topkentries:
            tmp_array = []
            tmp_array.append(key)
            tmp_array.append("")
            tmp_array.append(value)
            lexico_array.append(tmp_array)
        else:
            pattern_once += 1
            
                
    
            
    #f_out = open("/home/swalter/lementries","w")
    #for x in lexico_array:
    #    f_out.write(x[0]+"\n")
    #f_out.close()
    return lexico_array , pattern_once


    
    
def sort_array(array):
    'sort that the highest number comes first'
    return (sortby(array,2, True))


def sortby(somelist, n, bool):
    nlist = [(x[n], x) for x in somelist]
    nlist.sort(reverse=bool)
    return [val for (key, val) in nlist]

