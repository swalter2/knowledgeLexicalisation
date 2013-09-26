"""
Generates lemon lexicon entries out of given patterns
"""
from nltk.stem.wordnet import WordNetLemmatizer
from Util import Levenshtein
import Sparql
from Util import WordnetFunctions as wn
import StandardLexiconEntries
import ConfigParser
language = None

# 0 x _ nnp nnp _ 1 nsubj _ _  1 married _ vbd vbd _ 2 rcmod _ _  2 y _ nnp nnp _ 3 dobj _ _

def verbEntry(term,uri,marker):
    sparql = Sparql.Connection()
    term = term.split(" ")[1]
    term = checkForIngForm(term)
    entry = []
    wiktionary_informations = []
    try:
        wiktionary_informations = sparql.getWiktionaryInformations(term)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        wiktionary_informations = []
    if len(wiktionary_informations) == 0:
        
        if term.endswith("ed"):
#             term = term[:-2]
            entry.append(TransitiveFrame(term[:-1], uri,marker))
#             entry.append(AdjectivePPFrame(term[:-1], uri,marker))
            entry.append(TransitiveFrame(term[:-2], uri,marker))
#             entry.append(AdjectivePPFrame(term[:-2], uri,marker))
        elif term.endswith("s"):
            term = term[:-1]
            entry.append(TransitiveFrame(term, uri,marker))
#             entry.append(AdjectivePPFrame(term, uri,marker))
        else:
            entry.append(TransitiveFrame(term, uri,marker))
#             entry.append(AdjectivePPFrame(term, uri,marker))
    else:
        for e in wiktionary_informations:
            if e[0] == "verb" and "," not in e[1]:
                entry.append(TransitiveFrame(e[1], uri,marker))
                entry.append(AdjectivePPFrame(e[1], uri,marker))
#     print ("entry",entry)  
#     print  
    return entry

def englishMapping(pattern,uri):
    array = pattern.split("  ")
    print pattern
#     raw_input("wait")
    if len(array) == 3:
        print "in 3"
        
        if (" vbd" in array[1] or " vbn" in array[1] or " vbz" in array[1]) and (" rcmod" in array[1] or " null" in array[1]):
            print "case1"
            term = array[1]
            if len(term)<3:
                return None
            entry_list = verbEntry(term,uri,"")
            return entry_list
            
        if (" nn" in array[1])  and ("sub" in array[1] or "obj" in array[1] or " null" in array[1]): 
            print "case4"
            term = array[1]
            term = term.split(" ")[1]
            if len(term)<3:
                return None
            if term != "x" and term != "y":
                entry = NounPPFrame(term,uri,{})
                return [entry]
            
        if (" nn" in array[1]) and ("dep" in array[1] or " null" in array[1]): 
            print "case6 - nn case"
            term = array[1]
            if len(term)<3:
                return None
            entry_list = verbEntry(term,uri,"")
#             print
#             print
            return entry_list
        
#          if " nn "
            
    if len(array) == 4:
        print "in 4"
        if (" vbd" in array[1] or " vbn" in array[1] or " vbz" in array[1]) and (" rcmod" in array[1] or " null" in array[1]):
#         if (" vbd" in array[1] and " rcmod" in array[1]) or (" vbn" in array[1] and " rcmod" in array[1]):
            print "case2"
            marker = array[2]
            if " x " not in marker and " y " not in marker:
                 marker = marker.split(" ")[1]
            print ("marker",marker)
            term = array[1]
            if len(term)<3:
                return None
            entry_list = verbEntry(term,uri,marker)
#             print
#             print
            return entry_list
            
        if (" nn" in array[1]) and ("sub" in array[1] or "obj" in array[1] or " null" in array[1]): 
            print "case3"
            marker = array[2]
            hm = {}
            if " x " not in marker and " y " not in marker:
                 marker = marker.split(" ")[1]
                 hm[marker] = ""
            term = array[1]
            term = term.split(" ")[1]
            if len(term)<3:
                return None
            if term != "x" and term != "y":
                entry = NounPPFrame(term,uri,hm)
                return [entry]
            
        if (" nn" in array[1]) and ("dep" in array[1] or " null" in array[1]): 
            print "case5 - nn case"
            marker = array[2]
            if " x " not in marker and " y " not in marker:
                 marker = marker.split(" ")[1]
            print ("marker",marker)
            term = array[1]
            if len(term)<3:
                return None
            entry_list = verbEntry(term,uri,marker)
#             print
#             print
            return entry_list
            
    
    
    return []
# def englishMapping(pattern,uri):
#     sparql = Sparql.Connection()
#     marker = {}
#     lmtzr = WordNetLemmatizer()
#     term = ""
#     for item in pattern.split("  "):
#             
#         if ("in" in item.split(" ")[3].lower() or "to" in item.split(" ")[3].lower()) and item.split(" ")[1]!="x" and item.split(" ")[1]!="y":
#             marker[item.split(" ")[1]]=""
#             
#         elif item.split(" ")[1]!="x" and item.split(" ")[1]!="y":
#                 term += item+"  "
#     if term.endswith("  "):
#         term = term[:-2]
#                 
#  
#     entry_term = ""
#     if "  " in term:
#         for x in term.split("  "):
#             entry_term += x.split(" ")[1]+" "
#         if entry_term.endswith(" "):
#             entry_term = entry_term[:-1]
#     else:
#         entry_term = term.split(" ")[1]
#     
# 
#     if " vb" in term:
# #         if marker.has_key("to") or "vbn" in term  or "vbg" in term  or "vbd" in term  or marker.has_key("on"):
#         if entry_term.endswith("ing"):
#             entry_term = checkForIngForm(entry_term)
#             return [TransitiveFrame(entry_term, uri,marker)]
#         else:
#             wiktionary_informations = []
#             try:
#                 wiktionary_informations = sparql.getWiktionaryInformations(entry_term)
#             except:
#                 print "Unexpected error:", sys.exc_info()[0]
#                 wiktionary_informations = []
#             if len(wiktionary_informations) == 0:
#     #                 lemma = lmtzr.lemmatize(entry_term,"v")
#                 return [TransitiveFrame(entry_term, uri,marker)]
#     #                 return [AdjectivePredicateFrame(entry_term,uri, marker),TransitiveFrame(entry_term, uri,marker),TransitiveFrame(lemma, uri,marker)]
#             else:
#                 tmp = []
#                 for entry in wiktionary_informations:
#     #                     raw_input("wait")
#     # and "," not in entry[1]: in order to avoid entries like From  apperen, aperen, from  aparoir
#                     if entry[0] == "verb" and "," not in entry[1]:
#                         tmp.append(TransitiveFrame(entry[1], uri,marker))
#                     if entry[0] == "adjective" and "," not in entry[1]:
#                         tmp.append(AdjectivePredicateFrame(entry[1], uri,marker))
#                 return tmp
#                     
# #         else:
# #             return [TransitiveFrame(entry_term, uri,marker)]
# #             
# #         print
#     else:
#         if marker.has_key("of"):  
#             return [NounPossisiveFrame(entry_term,uri)]
#         else:
#             return [NounPPFrame(entry_term,uri,marker)]
#     return []
        

def germanMapping(pattern,uri):
    marker = {}
    term = ""
    print pattern
    for item in pattern.split("  "):
        item = item.lower()
        if (item.split(" ")[7] == "pp" or item.split(" ")[1]=="von" or item.split(" ")[1]=="mit")and item.split(" ")[1]!="x" and item.split(" ")[1]!="y":
            marker[item.split(" ")[1]]=""
            
        elif item.split(" ")[1]!="x" and item.split(" ")[1]!="y" and item.split(" ")[1]!="und" and  item.split(" ")[1]!="war" and item.split(" ")[1]!="sein" and  item.split(" ")[1]!="waren":
                term += item+"  "
    if term.endswith("  "):
        term = term[:-2]
                

    entry_term = ""
    if "  " in term:
        for x in term.split("  "):
            entry_term += x.split(" ")[1]+" "
        if entry_term.endswith(" "):
            entry_term = entry_term[:-1]
    else:
        entry_term = term.split(" ")[1]
    
    #in order to achieve a high recall, create for all 
    return [AdjectivePredicateFrame(entry_term,uri, marker),TransitiveFrame(entry_term, uri,marker),NounPossisiveFrame(entry_term,uri),NounPPFrame(entry_term,uri,marker)]

        
        
        
def createLexiconEntry(pattern,uri,Wiktionary, term = None):
    """
    As input this function retrieves a pattern, a URI and a Wiktionary (which is not used in the moment).
    For the pattern now it is determined, in which form of lemon lexicon entry it is transformed, using POS tag and parser informations.
    The pattern here is still in the CONLL format.
    In the moment this function is limited to AdjectivePredicateFrame, TransitiveFrame, NounPossisiveFrame, NounPPFrame
    """

#    print "In lexicon generation"
    if pattern[len(pattern)-2:] == "  ":
        pattern = pattern[:len(pattern)-2:]

    config = ConfigParser.ConfigParser()
    config.read('config.conf')
    global language
    
    if config.get('system_language', 'language') == "English":
        language = "English"
        return englishMapping(pattern,uri)
    elif config.get('system_language', 'language') == "German":
        language = "German"
        return germanMapping(pattern,uri)
    else:
        return None
        
    



def createClassEntry(uri,en_target_lexicon):
    """
    Creates a standard class entry for a given URI.
    As label for the entry, the label from the URI is taken (sparql.getLabel)
    """
    
    sparql = Sparql.Connection()
    label = sparql.getLabel(uri)[0]
    result_array = []
    array = wn.return_synsetsNoun(label)
    for entry in array:
        for x in StandardLexiconEntries.createLabel(entry,en_target_lexicon):
            x = x.replace("_"," ")

            lexEntry = "ClassNoun(\""+ x+"\",<"+uri+">)"
            result_array.append(lexEntry)
    return result_array




def NounPossisiveFrame(term,reference):
    """
    Creates an NounPossisiveFrame  entry for a given label and reference with a standard "of" marker
    """
    term = term.replace(";","")
    entry = "RelationalNoun(\""+term+"\",<"+reference+">, propSubj = PossessiveAdjunct, propObj  = CopulativeArg)"
    return entry

def NounPossisiveFrameWithoutMarker(term,reference):
    """
    Creates an NounPossisiveFrame  entry for a given label and reference, but without any marker
    """
    term = term.replace(";","")
    entry = "RelationalNoun(\""+term+"\",<"+reference+">, propSubj = PossessiveAdjunct, propObj  = CopulativeArg)"
    return entry

  
def TransitiveFrame(term, reference,marker):
    """
    Creates an TransitiveFrame entry for a given label, reference and marker
    """
    print ("Marker in transitive frame",marker)
    term = term.replace(";","")
# #     In order to increase, accuracy, use the marker.
# #     In order to increase Recall, do not use the marker and create only entries, without marker
    entry = "StateVerb(\""+term+"\",<"+reference+">, propSubj = DirectObject, propObj  = Subject)"
    
#     if len(marker) == 0 or marker.isalpha()== False:
#         entry = "StateVerb(\""+term+"\",<"+reference+">, propSubj = DirectObject, propObj  = Subject)"
#         return entry
#     else:
#         entry = "StateVerb(\""+term+"\",<"+reference+">,propObj  = PrepositionalObject(\""+marker+"\"))"


    return entry


def AdjectivePredicateFrame(term, reference, marker):
    """
    Creates an AdjectivePredicateFrame entry for a given label, reference and marker
    """
    
    term = term.replace(";","")
    entry = "RelationalAdjective(\""+term+"\",<"+reference+">, relationalArg = PrepositionalObject(\"to\"))"
    return entry


def AdjectivePPFrame(term, reference, marker):
    """
    Creates an AdjectivePPFrame entry for a given label, reference and marker
    """
    term = term.replace(";","")
    entry = "RelationalAdjective(\""+term+"\",<"+reference+">, relationalArg = PrepositionalObject(\"to\"))"
    return entry



def NounPPFrame(term,reference,marker):
    """
    Creates an NounPPFrame entry for a given label, reference and marker
    """
    marker_a = []
    for key in marker:
        marker_a.append(key)
    term = term.replace(";","")
    entry = ""
    #beim generieren der Pattern wird entschieden, was fuer ein frame gegeben ist, abhaengig dvon, ob eine praeposition gegeben ist oder nicht
    if len(marker) == 0 or marker.isalpha()== False:
        entry = "RelationalNoun(\""+term+"\",<"+reference+">, propSubj = PossessiveAdjunct, propObj  = CopulativeArg)"
        return entry
    else:
        entry = "RelationalNoun(\""+term+"\",<"+reference+">, propSubj = PrepositionalObject(\""+marker_a[0]+"\"), propObj  = CopulativeArg)"
        return entry



def checkForIngForm(string):
#     star",dbpedia:starring, check, if words then ends with twice the same letter, if so, remove last letter

    if string.endswith("ing"):
        string = string[:-3]
#         laenge = len(string)-1
#         a = string[laenge:]
#         b = string[laenge-1:-1]
#         
#         if a == b:
#             string = string[:-1]
        if string[:-1].endswith(string[-1:]):
            string = string[:-1]
        return string
        
        
    else:
        return string
    
