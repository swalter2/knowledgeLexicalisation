import LexiconGenerator, StandardLexiconEntries
import os, sys, ConfigParser
from Index import IndexUtils
from Util import  WordnetFunctions
import Sparql




def create_lexico_array(hm,uri,NumberOfPatterns, en_de_lexicon):
    print "Number of patterns: "+str(len(hm))
    config = ConfigParser.ConfigParser()
    config.read('config.conf')
    procentOfPatterns = config.getfloat("entries", "PatternProcent")
    topkentries = procentOfPatterns
    lexico_array = []
    sparql = Sparql.Connection()
    pattern_once = 0
    
    mapping_pattern_entry = {}
    
    
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
    patterns_without_entry = []

    for key, value_pattern in sorted(hm.iteritems(), key=lambda x:x[1], reverse = True):
        best_counter += 1
        """
        Different selecting strategies based on the lemon entries
        
        """
        try:
            entry_array = []
            entry_array=LexiconGenerator.createLexiconEntry(key, uri, False)
            for entry in entry_array:
                #print entry,value_pattern
                try:
                    if mapping_pattern_entry.has_key(entry):
                        tmp_entry = []
                        tmp_entry = mapping_pattern_entry[entry]
                        tmp_entry.append([key,value_pattern])
                        mapping_pattern_entry[entry]=tmp_entry
                    else:
                        mapping_pattern_entry[entry]=[[key,value_pattern]]
                except:
                    #print "pattern: "+entry
                    print "Unexpected error in mapping pattern to entry:", sys.exc_info()[0]
                    print "pattern: "+entry
                    print
                                                      
                
                
                if lem_entries_hm.has_key(entry):
                    value = lem_entries_hm[entry]
                    value += value_pattern
                    lem_entries_hm[entry] = value
                else:
                    lem_entries_hm[entry] = value_pattern

            if len(entry_array) == 0:
                patterns_without_entry.append([key,value_pattern])

        except:
            patterns_without_entry.append([key,value_pattern])

            
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
        if lem_counter <= topkentries:
            tmp_array = []
            tmp_array.append(key)
            tmp_array.append("")
            tmp_array.append(value)
            lexico_array.append(tmp_array)
        else:
            pattern_once += 1
            
                

    return lexico_array , pattern_once, patterns_without_entry, mapping_pattern_entry


    
    
def sort_array(array):
    'sort that the highest number comes first'
    return (sortby(array,2, True))


def sortby(somelist, n, bool):
    nlist = [(x[n], x) for x in somelist]
    nlist.sort(reverse=bool)
    return [val for (key, val) in nlist]

