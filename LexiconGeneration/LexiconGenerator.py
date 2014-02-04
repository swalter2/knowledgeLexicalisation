"""
Generates lemon lexicon entries out of given patterns
"""
#from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import WordNetLemmatizer
from Util import Levenshtein
import Sparql
from Util import WordnetFunctions as wn
import StandardLexiconEntries
import ConfigParser, sys
language = None
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet as wordnet



# >>> from nltk.corpus import wordnet as wn
# >>> wn.morphy('denied', wn.VERB)
# 'deny'
# >>> wn.morphy('commanded', wn.VERB)
# 'command'
# >>> wn.morphy('married', wn.VERB)
# 'marry'
# >>> wn.morphy('hello', wn.VERB)

def verbEntry(term,uri,marker):
    #stemmer = SnowballStemmer("english")
    #stemmer.stem("married")
    
    
    wnl = WordNetLemmatizer()
    hm = {}
    sparql = Sparql.Connection()
    if " " in term:
        term = term.split(" ")[1]
        
    tmp = wordnet.morphy(term, wordnet.VERB)
    if tmp != None and len(tmp)>2:
        hm[TransitiveFrame(tmp, uri,marker)] = ""
        
    else:

        stem = wnl.lemmatize(term)
        wiktionary_informations = sparql.getWiktionaryInformationsNEW(stem)
        for x in wiktionary_informations:
            if " + " in x[0] and "," not in x[0] and "*" not in x[0]:
                tmp = x[0].split(" + ")[0]
                if "Verb" in x[1] and len(tmp)>2:
                    hm[TransitiveFrame(tmp, uri,marker)] = ""

            elif "," not in x[0] and "*" not in x[0]:
                if "Verb" in x[1] and len(term)>2:
                    hm[TransitiveFrame(term, uri,marker)] = ""
    
        if len(wiktionary_informations) == 0 and len(stem)>2:
            hm[TransitiveFrame(stem, uri,marker)]  = ""
        
    entry = []
    for key in hm:
        entry.append(key)
            
    return entry
    

def englishMapping(pattern,uri):
#     uri = uri.replace("http://dbpedia.org/ontology/","dbpedia:")
    array = pattern.split("  ")

    if len(array) == 3:
        
        if (" vbd" in array[1] or " vbz" in array[1]) and (" rcmod" in array[1] or " null" in array[1]):
            term = array[1]
            if len(term)<3:
                return []
            entry_list = verbEntry(term,uri,"")
            return entry_list
        
        elif (" vbn" in array[1]) and (" dep" in array[1] or  " rcmod" in array[1] or " null" in array[1]):
            term = array[1]
            term = term.split(" ")[1]
            if len(term)<3:
                return []
            return [AdjectivePredicateFrameMarker(term,uri,"to")]
        
            
        elif (" nn" in array[1])  and ("sub" in array[1] or "obj" in array[1] or " null" in array[1]): 
            term = array[1]
            term = term.split(" ")[1]
            if len(term)<3:
                return []
            if term != "x" and term != "y":
                entry = NounPPFrame(term,uri,{})
                return [entry]
            
        elif (" nn" in array[1]) and ("dep" in array[1] or " null" in array[1]): 
            term = array[1]
            if len(term)<3:
                return []
            entry_list = verbEntry(term,uri,"")

            return entry_list

        
            
    if len(array) == 4:
            
        if (" vbd" in array[1] or " vbz" in array[1]) and (" dep" in array[1] or  " rcmod" in array[1] or " null" in array[1]):
            marker = array[2]
            if " x " not in marker and " y " not in marker:
                 marker = marker.split(" ")[1]
            term = array[1]
            if len(term)<3:
                return []
            entry_list = verbEntry(term,uri,marker)

            return entry_list
        
        elif (" vbn" in array[1]) and (" dep" in array[1] or  " rcmod" in array[1] or " null" in array[1]):
            marker = array[2]
            if " x " not in marker and " y " not in marker:
                 marker = marker.split(" ")[1]
            term = array[1]
            term = term.split(" ")[1]
            if len(term)<3:
                return []
            return [AdjectivePredicateFrameMarker(term,uri,marker)]
        
            
        elif (" nn" in array[1]) and ("sub" in array[1] or "obj" in array[1] or " null" in array[1]): 
            marker = array[2]
            hm = {}
            if " x " not in marker and " y " not in marker:
                 marker = marker.split(" ")[1]
                 hm[marker] = ""
            term = array[1]
            term = term.split(" ")[1]
            if len(term)<3:
                return []
            if term != "x" and term != "y":
                entry = NounPPFrame(term,uri,hm)
                return [entry]
            
        elif (" nn" in array[1]) and ("dep" in array[1] or " null" in array[1]): 
            marker = array[2]
            if " x " not in marker and " y " not in marker:
                 marker = marker.split(" ")[1]
            term = array[1]
            if len(term)<3:
                return []
            entry_list = verbEntry(term,uri,marker)
            return entry_list
            
    
    
    return []


        
def germanMapping(pattern,uri):
    array = pattern.split("  ")
    from nltk.stem.snowball import GermanStemmer
    stemmer = GermanStemmer()
    
    if len(array)== 3:
        if " n nn " in array[1]:
            marker = ""
            term = array[1]
            if " x " not in term and " y " not in term:
                 term = term.split(" ")[1]
            return [NounPPFrame(term,uri,marker)]
        
        if " v vvfin " in array[1]:
            marker = ""
            term = array[1]
            if " x " not in term and " y " not in term:
                 term = term.split(" ")[1]
            #return [TransitiveFrame(term, uri,marker)]
            return [TransitiveFrame(term, uri,marker),TransitiveFrame(stemmer.stem(term), uri,marker)]
        
        if " v vvpp " in array[1]:
            marker = ""
            term = array[1]
            if " x " not in term and " y " not in term:
                 term = term.split(" ")[1]
            return [AdjectivePredicateFrameMit(term,uri)]
        
    
    if len(array)==4:
        if " n nn " in array[1] and " prep appr " in array[2]:
            marker = array[2]
            if " x " not in marker and " y " not in marker:
                 marker = marker.split(" ")[1]
            term = array[1]
            if " x " not in term and " y " not in term:
                 term = term.split(" ")[1]
            return [NounPPFrame(term,uri,marker)]
        
        if " v vvfin " in array[1] and " n nn " in array[2]:
            marker = ""
            term = array[1]
            if " x " not in term and " y " not in term:
                 term = term.split(" ")[1]
            return [TransitiveFrame(term, uri,marker),TransitiveFrame(stemmer.stem(term), uri,marker)]
            #return [TransitiveFrame(term, uri,marker)]
        
        if " v vvpp " in array[1] and " prep appr " in array[2]:
            marker = array[2]
            if " x " not in marker and " y " not in marker:
                 marker = marker.split(" ")[1]
            term = array[1]
            if " x " not in term and " y " not in term:
                 term = term.split(" ")[1]
            return [AdjectivePredicateFrameMarker(term,uri,marker)]
        
    if len(array) == 5:
        if " v vvpp " in array[1] and " prep appr " in array[2]:
            marker = array[2]
            if " x " not in marker and " y " not in marker:
                 marker = marker.split(" ")[1]
            term = array[1]
            if " x " not in term and " y " not in term:
                 term = term.split(" ")[1]
            return [AdjectivePredicateFrameMarker(term,uri,marker)]
        
        
        
def spanishMapping(pattern,uri):
    return []
        
        
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
    elif config.get('system_language', 'language') == "Spanish":
        language = "Spanish"
        return spanishMapping(pattern,uri)
    else:
        return []
        
    




def createClassEntry(uri,label):
    """
    Creates a standard class entry for a given URI.
    As label for the entry, the label from the URI is taken (sparql.getLabel)
    """
    #sparql = Sparql.Connection()
    #label = sparql.getLabel(uri)[0]
#     uri = uri.replace("http://dbpedia.org/ontology/","dbpedia:")
    return "ClassNoun(\""+ label+"\",<"+uri+">)"



def NounPossisiveFrame(term,reference):
    """
    Creates an NounPossisiveFrame  entry for a given label and reference with a standard "of" marker
    """
#     reference = reference.replace("http://dbpedia.org/ontology/","dbpedia:")

    term = term.replace(";","")
    entry = "RelationalNoun(\""+term+"\",<"+reference+">, propSubj = PossessiveAdjunct, propObj  = CopulativeArg)"
    return entry

def NounPossisiveFrameWithoutMarker(term,reference):
    """
    Creates an NounPossisiveFrame  entry for a given label and reference, but without any marker
    """
#     reference = reference.replace("http://dbpedia.org/ontology/","dbpedia:")

    term = term.replace(";","")
    entry = "RelationalNoun(\""+term+"\",<"+reference+">, propSubj = PossessiveAdjunct, propObj  = CopulativeArg)"
    return entry

  
def TransitiveFrame(term, reference,marker):
    """
    Creates an TransitiveFrame entry for a given label, reference and marker
    """
    #print ("Marker in transitive frame",marker)
    term = term.replace(";","")
#     reference = reference.replace("http://dbpedia.org/ontology/","dbpedia:")

# #     In order to increase, accuracy, use the marker.
# #     In order to increase Recall, do not use the marker and create only entries, without marker
#     entry = "StateVerb(\""+term+"\","+reference+", propSubj = DirectObject, propObj  = Subject)"
    
    if len(marker) == 0 or marker.isalpha()== False:
        entry = "StateVerb(\""+term+"\",<"+reference+">, propSubj = DirectObject, propObj  = Subject)"
        return entry
    else:
        entry = "StateVerb(\""+term+"\",<"+reference+">,propObj  = PrepositionalObject(\""+marker+"\"))"


    return entry


def AdjectivePredicateFrame(term, reference, marker=None):
    """
    Creates an AdjectivePredicateFrame entry for a given label, reference and marker
    """
#     reference = reference.replace("http://dbpedia.org/ontology/","dbpedia:")

    term = term.replace(";","")
    entry = "RelationalAdjective(\""+term+"\",<"+reference+">,relationalArg = PrepositionalObject(\"to\"))"
    return entry


def AdjectivePredicateFrameMit(term, reference, marker=None):
    """
    Creates an AdjectivePredicateFrame entry for a given label, reference and marker
    """
#     reference = reference.replace("http://dbpedia.org/ontology/","dbpedia:")

    term = term.replace(";","")
    entry = "RelationalAdjective(\""+term+"\",<"+reference+">,relationalArg = PrepositionalObject(\"mit\"))"
    return entry

def AdjectivePredicateFrameMarker(term, reference, marker):
    """
    Creates an AdjectivePredicateFrame entry for a given label, reference and marker
    """
#     reference = reference.replace("http://dbpedia.org/ontology/","dbpedia:")

    term = term.replace(";","")
    if marker.isalpha()== True:
        entry = "RelationalAdjective(\""+term+"\",<"+reference+">, relationalArg = PrepositionalObject(\""+marker+"\"))"
        return entry
    else:
        return []


def AdjectivePPFrame(term, reference, marker):
    """
    Creates an AdjectivePPFrame entry for a given label, reference and marker
    """
#     reference = reference.replace("http://dbpedia.org/ontology/","dbpedia:")

    term = term.replace(";","")
    entry = "RelationalAdjective(\""+term+"\",<"+reference+">, relationalArg = PrepositionalObject(\"to\"))"
    return entry



def NounPPFrame(term,reference,marker):
    """
    Creates an NounPPFrame entry for a given label, reference and marker
    """
#     reference = reference.replace("http://dbpedia.org/ontology/","dbpedia:")

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
    if string.endswith("ing"):
        string = string[:-3]
#             string = string[:-1]
        if string[:-1].endswith(string[-1:]):
            string = string[:-1]
        return string
        
        
    else:
        return string
    
