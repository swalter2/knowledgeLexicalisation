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
    marker = {}
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
            lemma = lmtzr.lemmatize(entry_term,"v")
            return [AdjectivePredicateFrame(entry_term,uri, marker),TransitiveFrame(lemma, uri,marker)]
        else:
            return [TransitiveFrame(entry_term, uri,marker)]
            
        print
    else:
        if marker.has_key("of"):  
            return [NounPossisiveFrame(entry_term,uri)]
        else:
            return [NounPPFrame(entry_term,uri,marker)]
        

def germanMapping(pattern,uri):
    marker = {}
    term = ""
    for item in pattern.split("  "):
            
        if "pp" in item.split(" ")[7].lower() and item.split(" ")[1]!="x" and item.split(" ")[1]!="y":
            marker[item.split(" ")[1]]=""
            
        elif item.split(" ")[1]!="x" and item.split(" ")[1]!="y" and  item.split(" ")[1]!="war" and item.split(" ")[1]!="sein" and  item.split(" ")[1]!="waren":
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
            lemma = lmtzr.lemmatize(entry_term,"v")
            return [AdjectivePredicateFrame(entry_term,uri, marker),TransitiveFrame(lemma, uri,marker)]
        else:
            return [TransitiveFrame(entry_term, uri,marker)]
            
        print
    else:
        if marker.has_key("von"):  
            return [NounPossisiveFrame(entry_term,uri)]
        else:
            return [NounPPFrame(entry_term,uri,marker)]
        
        
        
def createLexiconEntry(pattern,uri,Wiktionary, term = None):
    """
    As input this function retrieves a pattern, a URI and a Wiktionary (which is not used in the moment).
    For the pattern now it is determined, in which form of lemon lexicon entry it is transformed, using POS tag and parser informations.
    The pattern here is still in the CONLL format.
    In the moment this function is limited to AdjectivePredicateFrame, TransitiveFrame, NounPossisiveFrame, NounPPFrame
    """
    lmtzr = WordNetLemmatizer()

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
        
    



def createClassEntry(uri,en_de_lexicon):
    """
    Creates a standard class entry for a given URI.
    As label for the entry, the label from the URI is taken (sparql.getLabel)
    """
    
    sparql = Sparql.Connection()
    label = sparql.getLabel(uri)[0]
    result_array = []
    array = wn.return_synsetsNoun(label)
    for entry in array:
        for x in StandardLexiconEntries.createLabel(entry,en_de_lexicon):
            x = x.replace("_"," ")
            lexEntry = ":"+x.replace(" ","").lower()+" a lemon:LexicalEntry ;\n"
            lexEntry += "lexinfo:partOfSpeech lexinfo:noun ;\n"
            lexEntry += "lemon:canonicalForm [ lemon:writtenRep \""+x.lower()+"\"@en ];\n"
            lexEntry += "lemon:sense [ lemon:reference <"+uri+"> ] ."
            result_array.append(lexEntry)
    return result_array




def NounPossisiveFrame(term,reference):
    """
    Creates an NounPossisiveFrame  entry for a given label and reference with a standard "of" marker
    """
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ];\n" 
    entry += "lemon:sense [ lemon:reference <"+reference+"> ;\n"
    entry += "lemon:subjOfProp :arg1 ;\n"
    entry += "lemon:objOfProp  :arg2 ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:NounPossessiveFrame ;\n"
    entry += "lexinfo:copulativeArg :arg2 ;\n"  
    entry += "lexinfo:possessiveAdjunct :arg1 ] ;\n"
    entry += "lexinfo:partOfSpeech lexinfo:noun .\n"
    if language == "German":
        entry += ":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \"von\"] ]."
    elif language == "English":
        entry += ":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \"of\"] ]."
    else:
        entry += ":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \"of\"] ]."
    return entry

def NounPossisiveFrameWithoutMarker(term,reference):
    """
    Creates an NounPossisiveFrame  entry for a given label and reference, but without any marker
    """
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ];\n" 
    entry += "lemon:sense [ lemon:reference <"+reference+"> ;\n"
    entry += "lemon:subjOfProp :arg1 ;\n"
    entry += "lemon:objOfProp  :arg2 ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:NounPossessiveFrame ;\n"
    entry += "lexinfo:copulativeArg :arg2;\n"
    entry += "lexinfo:possessiveAdjunct :arg1 ] ;\n"
    entry += "lexinfo:partOfSpeech lexinfo:noun ."
    return entry
  
def TransitiveFrame(term, reference,marker):
    """
    Creates an TransitiveFrame entry for a given label, reference and marker
    """
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
    #entry += "lemon:otherForm [ lemon:writtenRep "married"@en ;\n" 
    #entry += " lexinfo:verbMood lexinfo:participle ;\n"
    #entry += "lexinfo:aspect   lexinfo:perfective ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:TransitiveFrame ;\n"
    entry += "lexinfo:subject      :arg1 ;\n"
    entry += " lexinfo:directObject :arg2 ] ;\n"
    entry += "lemon:sense [ lemon:reference <"+reference+">;\n"
    entry += "lemon:subjOfProp :arg1;\n"
    entry += "lemon:objOfProp  :arg2 ] ;\n"
    if len(marker) == 0:
        entry += "lexinfo:partOfSpeech lexinfo:verb ."
    else:
        entry += "lexinfo:partOfSpeech lexinfo:verb .\n"
        for x in marker:
            entry +=":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry


def AdjectivePredicateFrame(term, reference, marker):
    """
    Creates an AdjectivePredicateFrame entry for a given label, reference and marker
    """
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:AdjectivePredicateFrame ;\n"
    entry += "lexinfo:copulativeSubject :arg1;\n"
    entry += "lexinfo:attributiveArg :arg1 ];\n"
    entry += "lemon:sense [ lemon:reference <"+reference+">;\n"
    entry += "lemon:subjOfProp :arg1;\n"
    entry += "lemon:objOfProp  :arg2 ] ;\n"
    if len(marker) == 0:
        entry += "lexinfo:partOfSpeech lexinfo:adjective ."
    else:
        entry += "lexinfo:partOfSpeech lexinfo:adjective .\n"
        for x in marker:
            entry +=":arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry

def AdjectivePPFrame(term, reference, marker):
    """
    Creates an AdjectivePPFrame entry for a given label, reference and marker
    """
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:AdjectivePPFrame ;\n"
    entry += "lexinfo:copulativeSubject   :arg1;\n"
    entry += "lexinfo:prepositionalObject :arg2 ];\n"
    entry += "lemon:sense [ lemon:reference <"+reference+"> ] ;\n"
    if len(marker) == 0:
        entry += "lexinfo:partOfSpeech lexinfo:adjective ."
    else:
        entry += "lexinfo:partOfSpeech lexinfo:adjective .\n"
        for x in marker:
            entry +=":arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry


def NounPPFrame(term,reference,marker):
    """
    Creates an NounPPFrame entry for a given label, reference and marker
    """
    term = term.replace(";","")
    entry = ":"+term.lower().replace(" ","_")+" a lemon:LexicalEntry ;\n"
    entry += "lemon:canonicalForm [ lemon:writtenRep \""+term+"\"@en ] ;\n"
    entry += "lemon:sense [ lemon:reference <"+reference+"> ;\n"
    entry += "lemon:subjOfProp :arg1 ;\n"
    entry += "lemon:objOfProp  :arg2 ] ;\n"
    entry += "lemon:synBehavior [ rdf:type lexinfo:NounPPFrame ;\n"
    entry += "lexinfo:copulativeArg :arg1 ;\n"
    entry += "lexinfo:prepositionalAdjunct :arg2] ;\n"
    if len(marker) == 0:
        entry += "lexinfo:partOfSpeech lexinfo:noun ."
    else:
        entry += "lexinfo:partOfSpeech lexinfo:noun .\n"
        for x in marker:
            entry +=":y_arg2 lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+x+"\"] ].\n"
    return entry


#def create_isocat():
#    hm = {}
#    
#    hm["nsubj"] = 2261 
#    hm["dobj"] = 2263
#    hm["iobj"] = 1310
#    hm["pobj"] = 4638
#    hm["dep"] = 2323
#    hm["amod"] = 2269
#    hm["det"] = 1272
#    hm["nn"] = 2261   
#    hm["prep"] = 2271
#    hm["punct"] = 1372
#    hm["root"] = 3460
#    hm["rel"] = 2317
#    hm["ref"] = 3751
#    hm["cc"] = 2272
#    hm["conj"] = 3132
#    hm["aux"] = 3095
#    
#    return hm


#def find_ontology_uri(pattern,ontologyEntryList):
#    'returns uri from travel ontology frame'
#    
#    if ontologyEntryList == None:
#        return None
#    
#    
#    nld = Levenshtein.calculate_normalized_levenshtein_distance
#    for key in ontologyEntryList:
#        if pattern.lower() == key.replace("http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#;","").lower():
#            return key
#        elif pattern.lower() in key.lower() or key.replace("http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#;","").lower() in pattern.lower():
#            return key
#        
#    for key in ontologyEntryList:
#        if nld(pattern.lower(),key.replace("http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#;","").lower()) >0.6:
#            return key
#        
#    if " " in pattern:
#        array_gold = pattern.split("_")
#        for item in array_gold:
#            for key in ontologyEntryList:
#                if nld(item.lower(),key.replace("http://www.semanticweb.org/ontologies/2012/4/Ontology1336387504255.owl#;","").lower()) >0.6:
#                    return key
#    return None

#def createNounPPFrameEntry(pattern,uri):
#    array = pattern.split("  ")
#    entry_term = ""
#    marker = []
#
#    for a in array:
#        if "x" not in a and "y" not in a and "nn" in a and ("dobj" in a or "nn" in a or "pobj" in a):
#            entry_term = a.split(" ")[1]
#
#        if ("in" in a.split(" ")[3] or "to" in a.split(" ")) and a.split(" ")[1]!="x" and a.split(" ")[1]!="y":
#
#            marker.append(a.split(" ")[1])
#        
#    if len(entry_term)<3:
#        return None
#               
#    entry = ":"+entry_term.replace(" ","").lower()+" a lemon:LexicalEntry ; "
#    entry +="\nlemon:canonicalForm [ lemon:writtenRep \""+entry_term.lower()+"\"@en ] ;\n"
#    entry +="lemon:synBehavior [ rdf:type lexinfo:NounPPFrame ;\n"
#    entry +="isocat:copulativeArg :xargument ;\n"
#    entry +="isocat:possessiveAdjunct :yargument ;\n"
#    entry +="] ;\n"
#    entry +="lemon:sense [ lemon:reference <"+uri+"> ;\n"
#    entry +="lemon:subjOfProp :xargument ;\n"
#    entry +="lemon:objOfProp :yargument ; ] ;\n"
#    entry +="lexinfo:partOfSpeech lexinfo:noun ."
#    if len(marker)>0:
#        entry +="\n:y_pobj lemon:marker [ lemon:canonicalForm [ lemon:writtenRep \""+marker[0]+"\"] ]."
#
#    return entry
#
#
#def createNounPPFrameEntryWordnet(uri):
#    sparql = Sparql.Connection()
#    label = sparql.getLabel(uri)[0]
#    result_array = []
#    array = wn.return_synsetsNoun(label)
#    
#    for a in array:
#        tag,tag_array = wn.return_Informations(a)
#        frame = None
#        partOfSpeech = None
#        
#        if tag == "VERB":
#            frame = "TransitiveFrame"
#            partOfSpeech = "verb"
#        elif tag == "NOUN":
#            frame = "NounPPFrame"
#            partOfSpeech = "noun"
#        elif tag == "ADJ":
#            frame = "AdjectivePPFrame"
#            partOfSpeech = "adjective"
#        elif tag == "NONE":
#            frame = "NounPPFrame"
#            partOfSpeech = "noun"
#        
#        for item in tag_array:
#            entry = ":"+item.lower().replace(" ","")+" a lemon:LexicalEntry ; "
#            entry +="\nlemon:canonicalForm [ lemon:writtenRep \""+item.lower()+"\"@en ] ;\n"
#            entry +="lemon:synBehavior [ rdf:type lexinfo:"+frame+" ;\n"
#            entry +="isocat:copulativeArg :x_nn ;\n"
#            entry +="isocat:DC-4638 :y_pobj ;\n"
#            entry +="] ;\n"
#            entry +="lemon:sense [ lemon:reference <"+uri+"> ;\n"
#            entry +="lemon:subjOfProp :x_nn ;\n"
#            entry +="lemon:objOfProp :y_pobj ; ] ;\n"
#            entry +="lexinfo:partOfSpeech lexinfo:"+partOfSpeech+" ."
#            result_array.append(entry) 
#
#    return result_array


#def createLexiconEntryForEntity(entity,uri):
#    
#    
#    entry = ":"+entity.replace(" ","").lower()+" a lemon:LexicalEntry ; \n lemon:canonicalForm [ lemon:writtenRep \""+entity.lower()+"\"@en ] ;"
#    entry += "lexinfo:partOfSpeech lexinfo:properNoun ; \n"
#    entry += "lemon:sense [ lemon:reference <"+uri+"> ].\n" 
#    return entry
