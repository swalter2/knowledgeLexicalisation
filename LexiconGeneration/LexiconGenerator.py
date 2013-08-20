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


def englishMapping(pattern,uri):
    sparql = Sparql.Connection()
    marker = {}
    lmtzr = WordNetLemmatizer()
    term = ""
    for item in pattern.split("  "):
            
        if ("in" in item.split(" ")[3].lower() or "to" in item.split(" ")[3].lower()) and item.split(" ")[1]!="x" and item.split(" ")[1]!="y":
            marker[item.split(" ")[1]]=""
            
        elif item.split(" ")[1]!="x" and item.split(" ")[1]!="y":
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
    

    if " vb" in term:
        if marker.has_key("to") or "vbn" in term  or "vbg" in term  or "vbd" in term  or marker.has_key("on"):
#             print "befor wiktionary informations"
            try:
                wiktionary_informations = sparql.getWiktionaryInformations(entry_term)
            except:
                print "Unexpected error:", sys.exc_info()[0]
#             print "after wiktionary informations"
            if wiktionary_informations == 0:
                lemma = lmtzr.lemmatize(entry_term,"v")
                return [TransitiveFrame(entry_term, uri,marker)]
#                 return [AdjectivePredicateFrame(entry_term,uri, marker),TransitiveFrame(entry_term, uri,marker),TransitiveFrame(lemma, uri,marker)]
            else:
                tmp = []
                for entry in wiktionary_informations:
                    print entry[0], entry[1]
#                     raw_input("wait")
                    if entry[0] == "verb":
                        tmp.append(TransitiveFrame(entry[1], uri,marker))
                    if entry[0] == "adjective":
                        tmp.append(AdjectivePredicateFrame(entry[1], uri,marker))
                return tmp
                    
        else:
            return [TransitiveFrame(entry_term, uri,marker)]
            
        print
    else:
        if marker.has_key("of"):  
            return [NounPossisiveFrame(entry_term,uri)]
        else:
            return [NounPPFrame(entry_term,uri,marker)]
    return []
        

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
#             lexEntry = ":"+x.replace(" ","").lower()+" a lemon:LexicalEntry ;\n"
#             lexEntry += "lexinfo:partOfSpeech lexinfo:noun ;\n"
#             lexEntry += "lemon:canonicalForm [ lemon:writtenRep \""+x.lower()+"\"@en ];\n"
#             lexEntry += "lemon:synBehavior [ rdf:type lexinfo:NounPredicateFrame ;\n"
#             lexEntry += "lexinfo:subject :arg ];\n"
#             lexEntry += "lemon:sense [ lemon:reference <"+uri+"> ;\n"
#             lexEntry += "lemon:isA :arg ] ." 
            result_array.append(lexEntry)
    return result_array




def NounPossisiveFrame(term,reference):
    """
    Creates an NounPossisiveFrame  entry for a given label and reference with a standard "of" marker
    """
    term = term.replace(";","")
    entry = "RelationalNoun(\""+term+"\",<"+reference+">, propSubj = PossessiveAdjunct, propObj  = CopulativeArg)"
#     entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
#     entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ];\n" 
#     entry += "lemon:sense [ lemon:reference <"+reference+"> ;\n"
#     entry += "lemon:subjOfProp :arg1 ;\n"
#     entry += "lemon:objOfProp  :arg2 ] ;\n"
#     entry += "lemon:synBehavior [ rdf:type lexinfo:NounPossessiveFrame ;\n"
#     entry += "lexinfo:copulativeArg :arg2 ;\n"  
#     entry += "lexinfo:possessiveAdjunct :arg1 ] ;\n"
#     entry += "lexinfo:partOfSpeech lexinfo:noun .\n"
#     if language == "German":
#         entry += ":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \"von\"] ]."
#     elif language == "English":
#         entry += ":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \"of\"] ]."
#     else:
#         entry += ":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \"of\"] ]."
    return entry

def NounPossisiveFrameWithoutMarker(term,reference):
    """
    Creates an NounPossisiveFrame  entry for a given label and reference, but without any marker
    """
    term = term.replace(";","")
    entry = "RelationalNoun(\""+term+"\",<"+reference+">, propSubj = PossessiveAdjunct, propObj  = CopulativeArg)"
     
#     entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
#     entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ];\n" 
#     entry += "lemon:sense [ lemon:reference <"+reference+"> ;\n"
#     entry += "lemon:subjOfProp :arg1 ;\n"
#     entry += "lemon:objOfProp  :arg2 ] ;\n"
#     entry += "lemon:synBehavior [ rdf:type lexinfo:NounPossessiveFrame ;\n"
#     entry += "lexinfo:copulativeArg :arg2;\n"
#     entry += "lexinfo:possessiveAdjunct :arg1 ] ;\n"
#     entry += "lexinfo:partOfSpeech lexinfo:noun ."
    return entry
  
def TransitiveFrame(term, reference,marker):
    """
    Creates an TransitiveFrame entry for a given label, reference and marker
    """

    term = term.replace(";","")
    if len(marker) == 0:
        entry = "StateVerb(\""+term+"\",<"+reference+">, propSubj = DirectObject, propObj  = Subject)"
        return entry
    else:
        entry = "StateVerb(\""+term+"\",<"+reference+">,propObj  = PrepositionalObject(\""+marker[0]+"\"))"
#     entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
#     entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
#     entry += "lemon:synBehavior [ rdf:type lexinfo:TransitiveFrame ;\n"
#     entry += "lexinfo:subject      :arg1 ;\n"
#     entry += " lexinfo:directObject :arg2 ] ;\n"
#     entry += "lemon:sense [ lemon:reference <"+reference+">;\n"
#     entry += "lemon:subjOfProp :arg1;\n"
#     entry += "lemon:objOfProp  :arg2 ] ;\n"
#     if len(marker) == 0:
#         entry += "lexinfo:partOfSpeech lexinfo:verb ."
#     else:
#         entry += "lexinfo:partOfSpeech lexinfo:verb .\n"
#         for x in marker:
#             entry +=":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry


def AdjectivePredicateFrame(term, reference, marker):
    """
    Creates an AdjectivePredicateFrame entry for a given label, reference and marker
    """
    
    term = term.replace(";","")
    entry = "RelationalAdjective(\""+term+"\",<"+reference+">, relationalArg = PrepositionalObject(\"to\"))"
    return entry
#     if len(marker) == 0:
#         entry = "RelationalAdjective(\""+term+"\",<"+reference+">)"
#         return entry
#     else:
#         entry = "RelationalAdjective(\""+term+"\",<"+reference+">, relationalArg = PrepositionalObject(\"to\"))"
#         return entry
    
    
#     term = term.replace(";","")
#     entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
#     entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
#     entry += "lemon:synBehavior [ rdf:type lexinfo:AdjectivePredicateFrame ;\n"
#     entry += "lexinfo:copulativeSubject :arg1;\n"
#     entry += "lexinfo:attributiveArg :arg1 ];\n"
#     entry += "lemon:sense [ lemon:reference <"+reference+">;\n"
#     entry += "lemon:subjOfProp :arg1;\n"
#     entry += "lemon:objOfProp  :arg2 ] ;\n"
#     if len(marker) == 0:
#         entry += "lexinfo:partOfSpeech lexinfo:adjective ."
#     else:
#         entry += "lexinfo:partOfSpeech lexinfo:adjective .\n"
#         for x in marker:
#             entry +=":arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry

def AdjectivePPFrame(term, reference, marker):
    """
    Creates an AdjectivePPFrame entry for a given label, reference and marker
    """
    term = term.replace(";","")
    entry = "RelationalAdjective(\""+term+"\",<"+reference+">, relationalArg = PrepositionalObject(\"to\"))"
    return entry

#     if len(marker) == 0:
#         entry = "RelationalAdjective(\""+term+"\",<"+reference+">)"
#         return entry
#     else:
#         entry = "RelationalAdjective(\""+term+"\",<"+reference+">, relationalArg = PrepositionalObject(\"to\"))"
#         return entry


#     entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
#     entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
#     entry += "lemon:synBehavior [ rdf:type lexinfo:AdjectivePPFrame ;\n"
#     entry += "lexinfo:copulativeSubject   :arg1;\n"
#     entry += "lexinfo:prepositionalObject :arg2 ];\n"
#     entry += "lemon:sense [ lemon:reference <"+reference+"> ] ;\n"
#     if len(marker) == 0:
#         entry += "lexinfo:partOfSpeech lexinfo:adjective ."
#     else:
#         entry += "lexinfo:partOfSpeech lexinfo:adjective .\n"
#         for x in marker:
#             entry +=":arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry


def NounPPFrame(term,reference,marker):
    """
    Creates an NounPPFrame entry for a given label, reference and marker
    """
    term = term.replace(";","")
    entry = ""
    #beim generieren der Pattern wird entschieden, was fuer ein frame gegeben ist, abhaengig dvon, ob eine praeposition gegeben ist oder nicht
    if len(marker) == 0:
        entry = "RelationalNoun(\""+term+"\",<"+reference+">, propSubj = PossessiveAdjunct, propObj  = CopulativeArg)"
        return entry
    else:
        entry = "RelationalNoun(\""+term+"\",<"+reference+">, propSubj = PrepositionalObject(\""+marker[0]+"\"), propObj  = CopulativeArg)"
        return entry
     
    
#     entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
#     entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
#     entry += "lemon:sense [ lemon:reference <"+reference+"> ;\n"
#     entry += "lemon:subjOfProp :arg1 ;\n"
#     entry += "lemon:objOfProp  :arg2 ] ;\n"
#     entry += "lemon:synBehavior [ rdf:type lexinfo:NounPPFrame ;\n"
#     entry += "lexinfo:copulativeArg :arg1 ;\n"
#     entry += "lexinfo:prepositionalAdjunct :arg2] ;\n"
#     if len(marker) == 0:
#         entry += "lexinfo:partOfSpeech lexinfo:noun ."
#     else:
#         entry += "lexinfo:partOfSpeech lexinfo:noun .\n"
#         for x in marker:
#             entry +=":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry

